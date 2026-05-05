"""
VLM Zero-Shot Image Classifier — Proof of Concept Runner
=========================================================
Goal   : Replace the hardcoded 700-character text-length threshold used to
         classify SME product images as "advertisement/label" vs "product"
         with a VLM zero-shot classifier.

Models : scb10x/typhoon2-qwen2vl-7b-vision-instruct  (primary)
         Qwen/Qwen2.5-VL-7B-Instruct                  (fallback)

Both are built on the Qwen2-VL architecture.
Typhoon2-Vision = Thai-optimised fine-tune of Qwen2-VL-7B.

Confidence mechanism
--------------------
We prompt the model to return structured JSON:
  { "label": "product|advertisement", "confidence": 0.0-1.0, "reasoning": "..." }

This is "self-reported" confidence — appropriate for a POC.  It is not a
calibrated probability; treat the 0.7 threshold as a tunable heuristic.

If VLM confidence < 0.7 → fall back to the 700-char text-length threshold
(char count loaded from the sidecar JSON written by generate_sample.py).

Usage
-----
  python poc_runner.py --help
  python poc_runner.py --image sample_outputs/sample_product.png
  python poc_runner.py --image sample_outputs/sample_ad_label.png --save-json
  python poc_runner.py --image path/to/img.jpg --model-id Qwen/Qwen2.5-VL-7B-Instruct
  python poc_runner.py --image path/to/img.jpg --load-4bit   # for <16 GB VRAM

Setup (uv)
----------
  uv sync
  uv run python poc_runner.py --image sample_outputs/sample_product.png

Thai medical OCR pipeline context
----------------------------------
  Stage 2: Layout Detection — this classifier sits between raw image and OCR,
  routing "product" images to lightweight OCR and "ad/label" images to a full
  text-extraction pipeline.  Typhoon2-Vision is Thai-aware, which is critical
  for Thai packaging text.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="VLM zero-shot classifier: product vs advertisement/label image",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              uv run python poc_runner.py --image sample_outputs/sample_product.png
              uv run python poc_runner.py --image sample_outputs/sample_ad_label.png --save-json
              uv run python poc_runner.py --image my_img.jpg --load-4bit --device cpu
        """),
    )
    p.add_argument(
        "--image", required=True,
        help="Path to an input image (PNG / JPG)",
    )
    p.add_argument(
        "--model-id",
        default="scb10x/typhoon2-qwen2vl-7b-vision-instruct",
        help=(
            "HuggingFace model ID. "
            "Primary: scb10x/typhoon2-qwen2vl-7b-vision-instruct "
            "Fallback: Qwen/Qwen2.5-VL-7B-Instruct"
        ),
    )
    p.add_argument(
        "--device", default=None,
        help="Device override: 'cuda', 'cpu'. Default: auto-detect CUDA first.",
    )
    p.add_argument(
        "--load-4bit", action="store_true",
        help="Load model in 4-bit quantisation via bitsandbytes (saves ~8 GB VRAM).",
    )
    p.add_argument(
        "--confidence-threshold", type=float, default=0.7,
        help="VLM confidence below which the 700-char fallback is used (default: 0.7).",
    )
    p.add_argument(
        "--char-threshold", type=int, default=700,
        help="Character count threshold for the legacy OCR rule (default: 700).",
    )
    p.add_argument(
        "--metadata-json", default=None,
        help=(
            "Path to sidecar JSON from generate_sample.py "
            "(default: sample_outputs/samples_metadata.json if it exists)."
        ),
    )
    p.add_argument(
        "--max-new-tokens", type=int, default=256,
        help="Max tokens to generate for the VLM response (default: 256).",
    )
    p.add_argument(
        "--save-json", action="store_true",
        help="Save classification result JSON to sample_outputs/<image_stem>_result.json",
    )
    return p


# ---------------------------------------------------------------------------
# Device resolution
# ---------------------------------------------------------------------------

REQUIRED_VRAM_GB = 15.0   # BF16 7B ≈ 14 GB; add headroom


def resolve_device(requested: str | None) -> str:
    try:
        import torch
    except ImportError:
        raise SystemExit("[ERROR] torch not installed. Run: uv sync")

    if requested is not None:
        device = requested
        print(f"[Device] Forced to: {device}")
        return device

    if not torch.cuda.is_available():
        print("[Device] CUDA not available — using CPU (inference will be slow).")
        return "cpu"

    # Validate sm arch for this build
    arch_list = torch.cuda.get_arch_list()
    props = torch.cuda.get_device_properties(0)
    sm = f"sm_{props.major}{props.minor}"
    vram_gb = props.total_memory / (1024 ** 3)

    print(f"[Device] GPU: {props.name}  arch={sm}  VRAM={vram_gb:.1f} GB")
    print(f"[Device] CUDA arch list: {arch_list}")

    if sm not in arch_list:
        print(
            f"[WARN] {sm} not in torch arch list — this PyTorch build may not support "
            f"your GPU. Fix: change torch index to pytorch-cu128 in pyproject.toml "
            f"and re-run: uv sync --reinstall-package torch"
        )
        print("[Device] Falling back to CPU.")
        return "cpu"

    if vram_gb < REQUIRED_VRAM_GB:
        print(
            f"[WARN] GPU has {vram_gb:.1f} GB VRAM but BF16 7B model needs ~{REQUIRED_VRAM_GB:.0f} GB. "
            f"Use --load-4bit to quantise to ~8 GB, or ensure you have enough VRAM."
        )

    return "cuda"


# ---------------------------------------------------------------------------
# Model loader
# ---------------------------------------------------------------------------

def _pick_model_class(model_id: str):
    """
    Typhoon2 → Qwen2VLForConditionalGeneration
    Qwen2.5-VL → Qwen2_5_VLForConditionalGeneration
    These are distinct classes in transformers.
    """
    try:
        from transformers import (
            Qwen2VLForConditionalGeneration,
            Qwen2_5_VLForConditionalGeneration,
            AutoProcessor,
        )
    except ImportError:
        raise SystemExit(
            "[ERROR] transformers not installed or too old. Run: uv sync"
        )

    model_id_lower = model_id.lower()
    if "qwen2.5" in model_id_lower or "qwen2_5" in model_id_lower:
        model_cls = Qwen2_5_VLForConditionalGeneration
        print(f"[Model] Using Qwen2_5_VLForConditionalGeneration for '{model_id}'")
    else:
        # Typhoon2 and Qwen2-VL both use Qwen2VLForConditionalGeneration
        model_cls = Qwen2VLForConditionalGeneration
        print(f"[Model] Using Qwen2VLForConditionalGeneration for '{model_id}'")

    return model_cls, AutoProcessor


def load_model(
    model_id: str,
    device: str,
    load_4bit: bool = False,
) -> tuple[Any, Any]:
    """Download (once) and initialise model + processor. Returns (model, processor)."""

    try:
        import torch
        from transformers import BitsAndBytesConfig
    except ImportError as exc:
        raise SystemExit(f"[ERROR] Missing dependency: {exc}. Run: uv sync")

    model_cls, AutoProcessor = _pick_model_class(model_id)

    bnb_config = None
    if load_4bit:
        print("[Model] Loading in 4-bit mode via bitsandbytes …")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )

    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    print(f"[Model] Loading '{model_id}' (this downloads ~14 GB on first run) …")
    try:
        model = model_cls.from_pretrained(
            model_id,
            torch_dtype=dtype if not load_4bit else "auto",
            device_map="auto" if device == "cuda" else None,
            quantization_config=bnb_config,
        )
    except Exception as exc:
        raise SystemExit(
            f"[ERROR] Failed to load model '{model_id}': {exc}\n"
            f"  - Check HuggingFace connectivity\n"
            f"  - Try --load-4bit for low-VRAM environments\n"
            f"  - Try --model-id Qwen/Qwen2.5-VL-7B-Instruct as fallback"
        )

    if device == "cpu" and not load_4bit:
        model = model.to("cpu")

    model.eval()

    # Pixel budget: 256×28×28 = 200704 px max  (keeps VRAM manageable)
    min_pixels = 64 * 28 * 28
    max_pixels = 256 * 28 * 28
    try:
        processor = AutoProcessor.from_pretrained(
            model_id,
            min_pixels=min_pixels,
            max_pixels=max_pixels,
        )
    except Exception as exc:
        raise SystemExit(f"[ERROR] Failed to load processor for '{model_id}': {exc}")

    print("[Model] Ready.")
    return model, processor


# ---------------------------------------------------------------------------
# Classification prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are an image classification assistant. "
    "Your task is to determine whether an image shows a plain product "
    "(e.g. a single packaged item, bottle, or object with minimal text) "
    "or an advertisement / product label "
    "(e.g. a flyer, label scan, or image containing extensive promotional text). "
    "Respond ONLY with a JSON object — no other text."
)

USER_PROMPT = (
    "Please classify this image.\n\n"
    "Return ONLY valid JSON in exactly this format:\n"
    "{\n"
    '  "label": "product" or "advertisement",\n'
    '  "confidence": <float between 0.0 and 1.0>,\n'
    '  "reasoning": "<one or two sentences explaining your decision>"\n'
    "}\n\n"
    "Rules:\n"
    '- "label" must be exactly "product" or "advertisement"\n'
    '- "confidence" must be a float (e.g. 0.85)\n'
    "- Do not include any text outside the JSON object"
)


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def run_inference(
    model: Any,
    processor: Any,
    image_path: Path,
    device: str,
    max_new_tokens: int = 256,
) -> str:
    """Run VLM inference on image_path. Returns the raw generated text."""
    try:
        import torch
        from PIL import Image
    except ImportError as exc:
        raise SystemExit(f"[ERROR] Missing dependency: {exc}")

    if not image_path.exists():
        raise SystemExit(f"[ERROR] Image not found: {image_path}")

    image = Image.open(image_path).convert("RGB")

    conversation = [
        {
            "role": "system",
            "content": [{"type": "text", "text": SYSTEM_PROMPT}],
        },
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": USER_PROMPT},
            ],
        },
    ]

    text_prompt = processor.apply_chat_template(
        conversation, add_generation_prompt=True
    )

    inputs = processor(
        text=[text_prompt],
        images=[image],
        padding=True,
        return_tensors="pt",
    )

    target_device = "cuda" if device == "cuda" else "cpu"
    inputs = {k: v.to(target_device) if hasattr(v, "to") else v for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,         # greedy — deterministic for reproducibility
            temperature=None,
            top_p=None,
        )

    # Strip the prompt tokens from the output
    input_len = inputs["input_ids"].shape[1]
    generated_ids = output_ids[:, input_len:]
    raw_text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True,
    )[0]

    return raw_text


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def parse_vlm_response(raw_text: str) -> dict:
    """
    Extract { label, confidence, reasoning } from the VLM response.
    Robust: tries json.loads first, then regex fallback.
    Returns a dict with keys: label, confidence, reasoning, parse_ok.
    """
    # Clean up potential markdown fences
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.MULTILINE).strip()
    cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE).strip()

    # Attempt 1: direct json.loads on the whole response
    try:
        data = json.loads(cleaned)
        label = str(data.get("label", "")).strip().lower()
        confidence = float(data.get("confidence", 0.0))
        reasoning = str(data.get("reasoning", ""))
        if label in ("product", "advertisement") and 0.0 <= confidence <= 1.0:
            return {
                "label": label,
                "confidence": confidence,
                "reasoning": reasoning,
                "parse_ok": True,
            }
    except (json.JSONDecodeError, ValueError, TypeError):
        pass

    # Attempt 2: extract JSON object via regex (handles extra text around it)
    json_match = re.search(r"\{[^{}]*\}", cleaned, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group())
            label = str(data.get("label", "")).strip().lower()
            confidence = float(data.get("confidence", 0.0))
            reasoning = str(data.get("reasoning", ""))
            if label in ("product", "advertisement") and 0.0 <= confidence <= 1.0:
                return {
                    "label": label,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "parse_ok": True,
                }
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

    # Attempt 3: heuristic keyword scan (last resort)
    label_guess = "unknown"
    confidence_guess = 0.0
    if re.search(r"\badvertisement\b|\bad\b|\blabel\b", cleaned, re.IGNORECASE):
        label_guess = "advertisement"
        confidence_guess = 0.5
    elif re.search(r"\bproduct\b", cleaned, re.IGNORECASE):
        label_guess = "product"
        confidence_guess = 0.5

    conf_match = re.search(r"0\.\d+", cleaned)
    if conf_match:
        confidence_guess = float(conf_match.group())

    return {
        "label": label_guess,
        "confidence": confidence_guess,
        "reasoning": f"[Parse failed — heuristic only] Raw: {cleaned[:200]}",
        "parse_ok": False,
    }


# ---------------------------------------------------------------------------
# 700-char fallback rule
# ---------------------------------------------------------------------------

def threshold_decision(char_count: int, threshold: int = 700) -> str:
    return "advertisement" if char_count > threshold else "product"


def load_char_count_from_metadata(image_path: Path, metadata_path: Path | None) -> int | None:
    """Look up approx_char_count for image_path in the sidecar metadata JSON."""
    candidates = []
    if metadata_path and metadata_path.exists():
        candidates.append(metadata_path)

    # Also check the default sidecar location
    default = image_path.parent / "samples_metadata.json"
    if default.exists():
        candidates.append(default)
    default2 = Path(__file__).parent / "sample_outputs" / "samples_metadata.json"
    if default2.exists():
        candidates.append(default2)

    for meta_path in candidates:
        try:
            records = json.loads(meta_path.read_text())
            for rec in records:
                # Match by filename (stem or full path)
                rec_path = Path(rec.get("filename", ""))
                if (
                    rec_path.name == image_path.name
                    or str(rec_path) == str(image_path)
                ):
                    return int(rec.get("approx_char_count", 0))
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_summary(
    image_path: Path,
    vlm_result: dict,
    char_count: int | None,
    char_threshold: int,
    confidence_threshold: float,
    final_label: str,
    fallback_used: bool,
    model_id: str,
) -> None:
    """Print a human-readable comparison table to stdout."""
    divider = "-" * 64
    print()
    print("=" * 64)
    print("  VLM Zero-Shot Classifier — Result")
    print("=" * 64)
    print(f"  Image        : {image_path.name}")
    print(f"  Model        : {model_id}")
    print(divider)

    # VLM result
    vlm_label = vlm_result["label"]
    vlm_conf = vlm_result["confidence"]
    parse_ok = vlm_result["parse_ok"]
    reasoning = vlm_result["reasoning"]

    print(f"  VLM label    : {vlm_label:<15}  confidence={vlm_conf:.2f}")
    print(f"  Parse OK     : {'yes' if parse_ok else 'NO (heuristic fallback)'}")
    print(f"  Reasoning    :")
    for line in textwrap.wrap(reasoning, width=58, initial_indent="    ", subsequent_indent="    "):
        print(line)
    print(divider)

    # 700-char rule
    if char_count is not None:
        thresh_label = threshold_decision(char_count, char_threshold)
        print(f"  700-char rule: {thresh_label:<15}  (char_count={char_count}, threshold={char_threshold})")
    else:
        thresh_label = "N/A (no OCR data)"
        print(f"  700-char rule: {thresh_label}")
    print(divider)

    # Agreement
    if char_count is not None:
        agree = (vlm_label == thresh_label)
        agree_str = "AGREE" if agree else "DISAGREE"
        print(f"  Agreement    : {agree_str}")
    print(divider)

    # Fallback logic
    if fallback_used:
        print(f"  [FALLBACK]   VLM confidence {vlm_conf:.2f} < {confidence_threshold} threshold.")
        print(f"               Final decision deferred to 700-char rule: {final_label.upper()}")
    else:
        print(f"  Final label  : {final_label.upper()}  (VLM decision, confidence sufficient)")

    print("=" * 64)
    print()


def save_result_json(
    out_dir: Path,
    image_path: Path,
    vlm_result: dict,
    char_count: int | None,
    final_label: str,
    fallback_used: bool,
    model_id: str,
    char_threshold: int,
    confidence_threshold: float,
) -> Path:
    result = {
        "image": str(image_path),
        "model_id": model_id,
        "vlm_label": vlm_result["label"],
        "vlm_confidence": vlm_result["confidence"],
        "vlm_reasoning": vlm_result["reasoning"],
        "vlm_parse_ok": vlm_result["parse_ok"],
        "char_count": char_count,
        "char_threshold": char_threshold,
        "confidence_threshold": confidence_threshold,
        "threshold_decision": threshold_decision(char_count, char_threshold) if char_count is not None else None,
        "final_label": final_label,
        "fallback_used": fallback_used,
    }
    out_path = out_dir / f"{image_path.stem}_result.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"[INFO] Result saved: {out_path}")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    image_path = Path(args.image).resolve()
    if not image_path.exists():
        parser.error(f"Image not found: {image_path}")

    out_dir = Path(__file__).parent / "sample_outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1 — resolve device
    device = resolve_device(args.device)

    # Step 2 — load model
    model, processor = load_model(args.model_id, device, load_4bit=args.load_4bit)

    # Step 3 — run inference
    print(f"\n[Inference] Classifying: {image_path.name}")
    raw_text = run_inference(model, processor, image_path, device, args.max_new_tokens)
    print(f"[Inference] Raw VLM output:\n  {raw_text[:400]}")

    # Step 4 — parse response
    vlm_result = parse_vlm_response(raw_text)

    # Step 5 — load char count from sidecar metadata (if available)
    metadata_path = Path(args.metadata_json) if args.metadata_json else None
    char_count = load_char_count_from_metadata(image_path, metadata_path)
    if char_count is None:
        print(
            "[WARN] No char count found in sidecar metadata — "
            "700-char fallback comparison will show N/A. "
            "Run generate_sample.py first to create metadata."
        )

    # Step 6 — fallback decision
    vlm_conf = vlm_result["confidence"]
    fallback_used = vlm_conf < args.confidence_threshold

    if fallback_used:
        if char_count is not None:
            final_label = threshold_decision(char_count, args.char_threshold)
        else:
            # No char count available — stick with VLM despite low confidence
            print(
                "[WARN] VLM confidence is low but no char count available for fallback. "
                "Using VLM label anyway."
            )
            final_label = vlm_result["label"]
            fallback_used = False
    else:
        final_label = vlm_result["label"]

    # Step 7 — print summary
    print_summary(
        image_path=image_path,
        vlm_result=vlm_result,
        char_count=char_count,
        char_threshold=args.char_threshold,
        confidence_threshold=args.confidence_threshold,
        final_label=final_label,
        fallback_used=fallback_used,
        model_id=args.model_id,
    )

    # Step 8 — optionally save JSON
    if args.save_json:
        save_result_json(
            out_dir=out_dir,
            image_path=image_path,
            vlm_result=vlm_result,
            char_count=char_count,
            final_label=final_label,
            fallback_used=fallback_used,
            model_id=args.model_id,
            char_threshold=args.char_threshold,
            confidence_threshold=args.confidence_threshold,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
