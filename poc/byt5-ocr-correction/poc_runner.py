"""
ByT5-small — OCR Post-Correction POC
======================================
Stage 4: Post-correction (character-level seq2seq).

ByT5 operates at the byte level — no tokenizer vocabulary needed.
This is ideal for OCR error correction because:
  - Character-level substitutions (ก→ท, า→ๅ) are natural
  - Works across Thai + English without separate tokenizers
  - Small model (~300 MB) is fast for inference

Usage:
  uv run python poc_runner.py --input sample_outputs/sample_ocr_pairs.json
  uv run python poc_runner.py --input pairs.json --save-json
  uv run python poc_runner.py --text "ผลตรวจเลือค ปทติ"
"""

import argparse
import json
import sys
import time
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="ByT5 OCR post-correction POC")
    p.add_argument("--input", help="JSON file with noisy/clean pairs")
    p.add_argument("--text", help="Single noisy text to correct")
    p.add_argument("--model-name", default="google/byt5-small", help="HuggingFace model ID")
    p.add_argument("--device", default=None, help="Device: 'cuda', 'cpu', or None=auto")
    p.add_argument("--max-length", type=int, default=256, help="Max generation length")
    p.add_argument("--output-dir", default="sample_outputs", help="Output directory")
    p.add_argument("--save-json", action="store_true", help="Save corrections as JSON")
    return p


def resolve_device(requested: str | None) -> str:
    import torch

    if requested is not None:
        device = requested
    elif torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    if device.startswith("cuda") and torch.cuda.is_available():
        idx = 0
        name = torch.cuda.get_device_name(idx)
        cap = torch.cuda.get_device_capability(idx)
        vram = torch.cuda.get_device_properties(idx).total_memory / (1024**3)
        arch_list = torch.cuda.get_arch_list()
        sm = f"sm_{cap[0]}{cap[1]}"
        print(f"[device] {name}  sm={sm}  VRAM={vram:.1f} GB")
        if sm not in arch_list:
            print(f"[WARN] {sm} not in torch arch list {arch_list}")
            print("       Falling back to CPU.")
            return "cpu"
    else:
        print(f"[device] {device}")

    return device


def load_model(model_name: str, device: str):
    try:
        from transformers import AutoTokenizer, T5ForConditionalGeneration
    except ImportError:
        sys.exit("[ERROR] transformers not installed. Run: uv sync")

    print(f"[1/3] Loading ByT5 model  {model_name}  …")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    model.to(device)
    model.eval()
    print(f"      Model loaded  params={sum(p.numel() for p in model.parameters()) / 1e6:.0f}M")
    return model, tokenizer


def correct_text(model, tokenizer, noisy_text: str, device: str, max_length: int) -> str:
    """Run ByT5 to correct a single noisy OCR text.

    Note: ByT5-small is a *pretrained* model, NOT fine-tuned for OCR correction.
    This POC demonstrates the inference pipeline. For production quality,
    fine-tune on (noisy, clean) OCR text pairs.
    """
    prefix = "correct OCR: "
    input_text = prefix + noisy_text

    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    import torch
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=max_length)

    corrected = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected


def run_batch(model, tokenizer, pairs: list[dict], device: str, max_length: int) -> list[dict]:
    results = []
    for i, pair in enumerate(pairs, 1):
        noisy = pair["noisy"]
        clean = pair.get("clean", "")
        t0 = time.perf_counter()
        corrected = correct_text(model, tokenizer, noisy, device, max_length)
        elapsed = time.perf_counter() - t0
        results.append({
            "noisy": noisy,
            "corrected": corrected,
            "expected": clean,
            "match": corrected.strip() == clean.strip() if clean else None,
            "time_s": round(elapsed, 3),
        })
    return results


def print_summary(results: list[dict]) -> None:
    print(f"\n{'─' * 80}")
    print(f"  ByT5 OCR Post-Correction  →  {len(results)} samples")
    print(f"{'─' * 80}")
    for i, r in enumerate(results, 1):
        status = "✓" if r.get("match") else "✗" if r.get("match") is False else "?"
        print(f"\n  [{i:02d}] {status}  {r['time_s']:.2f}s")
        print(f"    noisy:     {r['noisy'][:70]}")
        print(f"    corrected: {r['corrected'][:70]}")
        if r["expected"]:
            print(f"    expected:  {r['expected'][:70]}")

    if any(r.get("match") is not None for r in results):
        matches = sum(1 for r in results if r.get("match"))
        total = sum(1 for r in results if r.get("match") is not None)
        print(f"\n  Accuracy: {matches}/{total} ({matches/total*100:.0f}%)")
    print(f"{'─' * 80}\n")

    print("  NOTE: ByT5-small is pretrained only (not fine-tuned for OCR correction).")
    print("  For production, fine-tune on Thai medical OCR error pairs.\n")


def save_outputs(results: list[dict], output_dir: Path, save_json: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    txt_out = output_dir / "corrections.txt"
    lines = []
    for r in results:
        lines.append(f"NOISY: {r['noisy']}")
        lines.append(f"FIXED: {r['corrected']}")
        lines.append("")
    txt_out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[3/3] Corrections saved  →  {txt_out}")

    if save_json:
        json_out = output_dir / "corrections.json"
        json_out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"      JSON saved  →  {json_out}")


def main() -> None:
    args = build_parser().parse_args()

    if not args.input and not args.text:
        sys.exit("[ERROR] Provide --input (JSON file) or --text (single string)")

    device = resolve_device(args.device)
    model, tokenizer = load_model(args.model_name, device)

    if args.text:
        pairs = [{"noisy": args.text, "clean": ""}]
    else:
        input_path = Path(args.input).resolve()
        if not input_path.exists():
            sys.exit(f"[ERROR] Input file not found: {input_path}")
        pairs = json.loads(input_path.read_text(encoding="utf-8"))

    print(f"[2/3] Correcting {len(pairs)} samples …")
    results = run_batch(model, tokenizer, pairs, device, args.max_length)
    print_summary(results)
    save_outputs(results, Path(args.output_dir), args.save_json)


if __name__ == "__main__":
    main()
