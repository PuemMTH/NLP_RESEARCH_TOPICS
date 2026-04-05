"""
GOT-OCR2.0 — Proof of Concept Runner
======================================
Stage 3: Text Recognition (VLM-based end-to-end OCR).

Uses the HuggingFace transformers integration: stepfun-ai/GOT-OCR-2.0-hf
Supports plain OCR and formatted OCR (Markdown/LaTeX output).

Usage:
  uv run python poc_runner.py --image sample_outputs/sample_doc.png
  uv run python poc_runner.py --image doc.png --mode format --save-json
"""

import argparse
import json
import sys
import time
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="GOT-OCR2.0 POC — VLM end-to-end OCR")
    p.add_argument("--image", required=True, help="Path to input document image")
    p.add_argument("--mode", choices=["ocr", "format"], default="ocr",
                   help="'ocr' = plain text, 'format' = structured markdown/latex")
    p.add_argument("--model-name", default="stepfun-ai/GOT-OCR-2.0-hf",
                   help="HuggingFace model ID")
    p.add_argument("--device", default=None, help="Device: 'cuda', 'cpu', or None=auto")
    p.add_argument("--output-dir", default="sample_outputs", help="Output directory")
    p.add_argument("--save-json", action="store_true", help="Save result as JSON")
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
            print("       Falling back to CPU. Reinstall torch with cu128 for Blackwell.")
            return "cpu"
    else:
        print(f"[device] {device}")

    return device


def load_model(model_name: str, device: str):
    try:
        from transformers import AutoModelForImageTextToText, AutoProcessor
    except ImportError:
        sys.exit("[ERROR] transformers not installed. Run: uv sync")

    import torch
    print(f"[1/3] Loading GOT-OCR2 model  {model_name}  …")
    dtype = torch.bfloat16 if device != "cpu" else torch.float32
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForImageTextToText.from_pretrained(
        model_name,
        torch_dtype=dtype,
        device_map=device,
        low_cpu_mem_usage=True,
    )
    model.eval()
    print(f"      Model loaded  dtype={dtype}")
    return model, processor


def run_inference(model, processor, image_path: Path, mode: str) -> str:
    """mode='ocr' = plain text, mode='format' = structured Markdown/LaTeX output."""
    import torch
    print(f"[2/3] Running GOT-OCR2  mode={mode}  on  {image_path.name}  …")
    t0 = time.perf_counter()
    use_format = (mode == "format")
    inputs = processor(str(image_path), return_tensors="pt", format=use_format).to(model.device)
    with torch.no_grad():
        generate_ids = model.generate(
            **inputs,
            do_sample=False,
            tokenizer=processor.tokenizer,
            stop_strings="<|im_end|>",
            max_new_tokens=4096,
        )
    text = processor.decode(
        generate_ids[0, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
    )
    elapsed = time.perf_counter() - t0
    print(f"      Inference: {elapsed:.1f}s")
    return text


def print_summary(text: str, image_name: str, mode: str) -> None:
    lines = text.strip().split("\n")
    print(f"\n{'─' * 70}")
    print(f"  GOT-OCR2.0  mode={mode}  →  {image_name}")
    print(f"  Output lines: {len(lines)}   chars: {len(text)}")
    print(f"{'─' * 70}")
    for line in lines[:30]:
        print(f"  {line}")
    if len(lines) > 30:
        print(f"  … ({len(lines) - 30} more lines)")
    print(f"{'─' * 70}\n")


def save_outputs(text: str, image_path: Path, output_dir: Path, mode: str, save_json: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_path.stem

    txt_out = output_dir / f"{stem}_ocr_{mode}.txt"
    txt_out.write_text(text, encoding="utf-8")
    print(f"[3/3] OCR text saved  →  {txt_out}")

    if save_json:
        json_out = output_dir / f"{stem}_result_{mode}.json"
        payload = {
            "image": str(image_path),
            "mode": mode,
            "num_lines": len(text.strip().split("\n")),
            "num_chars": len(text),
            "text": text,
        }
        json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"      JSON saved  →  {json_out}")


def main() -> None:
    args = build_parser().parse_args()
    image_path = Path(args.image).resolve()
    if not image_path.exists():
        sys.exit(f"[ERROR] Image not found: {image_path}")

    device = resolve_device(args.device)
    model, processor = load_model(args.model_name, device)
    text = run_inference(model, processor, image_path, args.mode)
    print_summary(text, image_path.name, args.mode)
    save_outputs(text, image_path, Path(args.output_dir), args.mode, args.save_json)

    if not text.strip():
        print("[WARN] No text detected")


if __name__ == "__main__":
    main()
