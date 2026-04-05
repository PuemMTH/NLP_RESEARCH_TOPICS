"""
EasyOCR Thai+English — Proof of Concept Runner
================================================
Stage 3: Text Recognition in the Thai Medical OCR Pipeline.

Uses EasyOCR with Thai + English language packs to read text
from document images — especially medical forms mixing both scripts.

Usage:
  uv run python poc_runner.py --image sample_outputs/sample_doc.png
  uv run python poc_runner.py --image doc.png --save-json --device cpu
"""

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="EasyOCR Thai+EN POC — text recognition")
    p.add_argument("--image", required=True, help="Path to input document image")
    p.add_argument("--langs", default="th,en", help="Comma-separated language codes (default: th,en)")
    p.add_argument("--device", default=None, help="'cpu' or '0' for GPU (default: auto)")
    p.add_argument("--output-dir", default="sample_outputs", help="Output directory")
    p.add_argument("--save-json", action="store_true", help="Save detections as JSON")
    return p


def resolve_device(requested: str | None) -> str:
    import torch

    if requested is not None:
        device = requested
        if device != "cpu" and not torch.cuda.is_available():
            print(f"[WARN] --device {device} requested but CUDA not available; falling back to cpu")
            device = "cpu"
    elif torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    if device != "cpu":
        props = torch.cuda.get_device_properties(int(device))
        sm_str = f"sm_{props.major}{props.minor}"
        arch_list = torch.cuda.get_arch_list()
        if sm_str not in arch_list:
            print(f"[WARN] GPU {props.name} ({sm_str}) not in arch list {arch_list}; falling back to cpu")
            print("       Fix: change pyproject.toml torch index to pytorch-cu128 and re-sync")
            device = "cpu"
        else:
            vram = props.total_memory / 1024 ** 3
            print(f"[device] CUDA:{device}  {props.name}  ({sm_str})  ({vram:.1f} GB VRAM)")

    if device == "cpu":
        print("[device] cpu")

    return device


def load_model(langs: list[str], use_gpu: bool):
    try:
        import easyocr
    except ImportError:
        sys.exit("[ERROR] easyocr not installed. Run: uv sync")

    print(f"[1/3] Loading EasyOCR reader  langs={langs}  gpu={use_gpu} …")
    reader = easyocr.Reader(langs, gpu=use_gpu)
    print("      Reader loaded.")
    return reader


def run_inference(reader, image_path: Path) -> list:
    print(f"[2/3] Running OCR on  {image_path.name}  …")
    results = reader.readtext(str(image_path))
    return results


def parse_detections(results: list) -> list[dict]:
    detections = []
    for bbox, text, conf in results:
        flat = [coord for pt in bbox for coord in pt]
        x_coords = flat[0::2]
        y_coords = flat[1::2]
        detections.append({
            "text": text,
            "confidence": round(float(conf), 4),
            "bbox_xyxy": [
                round(float(min(x_coords)), 1),
                round(float(min(y_coords)), 1),
                round(float(max(x_coords)), 1),
                round(float(max(y_coords)), 1),
            ],
        })
    detections.sort(key=lambda d: (d["bbox_xyxy"][1], d["bbox_xyxy"][0]))
    return detections


def print_summary(detections: list[dict], image_name: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  EasyOCR  →  {image_name}")
    print(f"  Text regions: {len(detections)}")
    print(f"{'─' * 70}")
    for i, det in enumerate(detections, 1):
        text_preview = det["text"][:50] + ("…" if len(det["text"]) > 50 else "")
        x1, y1, x2, y2 = det["bbox_xyxy"]
        print(f"  [{i:02d}] conf={det['confidence']:.3f}  ({x1:.0f},{y1:.0f})→({x2:.0f},{y2:.0f})  {text_preview}")
    print(f"{'─' * 70}\n")


def save_outputs(
    detections: list[dict],
    image_path: Path,
    output_dir: Path,
    save_json: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_path.stem

    # Full text dump
    txt_out = output_dir / f"{stem}_ocr.txt"
    full_text = "\n".join(d["text"] for d in detections)
    txt_out.write_text(full_text, encoding="utf-8")
    print(f"[3/3] OCR text saved  →  {txt_out}")

    if save_json:
        json_out = output_dir / f"{stem}_detections.json"
        payload = {
            "image": str(image_path),
            "total_regions": len(detections),
            "detections": detections,
        }
        json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"      JSON detections saved  →  {json_out}")


def main() -> None:
    args = build_parser().parse_args()
    image_path = Path(args.image).resolve()

    if not image_path.exists():
        sys.exit(f"[ERROR] Image not found: {image_path}")

    device = resolve_device(args.device)
    langs = [l.strip() for l in args.langs.split(",")]
    use_gpu = device != "cpu"

    reader = load_model(langs, use_gpu)
    results = run_inference(reader, image_path)
    detections = parse_detections(results)
    print_summary(detections, image_path.name)
    save_outputs(detections, image_path, Path(args.output_dir), args.save_json)

    if not detections:
        print("[WARN] No text detected — check image quality")


if __name__ == "__main__":
    main()
