"""
PaddleOCR v5 — Proof of Concept Runner (HuggingFace transformers backend)
==========================================================================
Stage 3: Text Recognition using PP-OCRv5 via HuggingFace transformers.

Two-stage pipeline:
  1. Detection  — PPOCRV5ServerDetForObjectDetection → text bounding boxes
  2. Recognition — PPOCRV5ServerRecForTextRecognition → text per crop

Models (safetensors variants with preprocessor_config.json):
  - Det: PaddlePaddle/PP-OCRv5_server_det_safetensors
  - Rec: PaddlePaddle/PP-OCRv5_server_rec_safetensors

Usage:
  uv run python poc_runner.py --image sample_outputs/sample_doc.png
  uv run python poc_runner.py --image doc.png --save-json
"""

import argparse
import json
import sys
import time
from pathlib import Path

DET_MODEL_ID = "PaddlePaddle/PP-OCRv5_server_det_safetensors"
REC_MODEL_ID = "PaddlePaddle/PP-OCRv5_server_rec_safetensors"


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="PP-OCRv5 POC — det+rec via transformers")
    p.add_argument("--image", required=True, help="Path to input document image")
    p.add_argument("--device", default=None, help="Device: 'cuda', 'cpu', or None=auto")
    p.add_argument("--output-dir", default="sample_outputs", help="Output directory")
    p.add_argument("--save-json", action="store_true", help="Save detections as JSON")
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


def load_models(device: str):
    try:
        import torch
        from transformers import (
            AutoImageProcessor,
            PPOCRV5ServerDetForObjectDetection,
            PPOCRV5ServerRecForTextRecognition,
        )
    except ImportError:
        sys.exit("[ERROR] transformers not installed. Run: uv sync")

    print(f"[1/3] Loading PP-OCRv5 models …")
    print(f"      det = {DET_MODEL_ID}")
    print(f"      rec = {REC_MODEL_ID}")

    det_proc = AutoImageProcessor.from_pretrained(DET_MODEL_ID)
    det_model = PPOCRV5ServerDetForObjectDetection.from_pretrained(DET_MODEL_ID)
    det_model.to(device).eval()

    rec_proc = AutoImageProcessor.from_pretrained(REC_MODEL_ID)
    rec_model = PPOCRV5ServerRecForTextRecognition.from_pretrained(REC_MODEL_ID)
    rec_model.to(device).eval()

    print("      Models loaded.")
    return (det_proc, det_model), (rec_proc, rec_model)


def run_inference(det_bundle, rec_bundle, image_path: Path, device: str) -> list[dict]:
    import torch
    from PIL import Image

    det_proc, det_model = det_bundle
    rec_proc, rec_model = rec_bundle

    print(f"[2/3] Running PP-OCRv5 on  {image_path.name}  …")
    t0 = time.perf_counter()

    image = Image.open(image_path).convert("RGB")
    orig_w, orig_h = image.size

    # --- Stage 1: Detection ---
    det_inputs = det_proc(images=image, return_tensors="pt")
    det_inputs = {k: v.to(device) for k, v in det_inputs.items()}

    with torch.no_grad():
        det_outputs = det_model(**det_inputs)

    target_sizes = torch.tensor([[orig_h, orig_w]], device=device)
    results = det_proc.post_process_object_detection(
        det_outputs, target_sizes=target_sizes,
    )[0]

    polygons = results["boxes"]  # (N, 4, 2) — 4-corner polygons [x, y]
    det_scores = results["scores"]  # (N,)

    # --- Stage 2: Recognition per crop ---
    detections = []
    for i in range(len(polygons)):
        poly = polygons[i]  # (4, 2)
        xs = poly[:, 0]
        ys = poly[:, 1]
        x1, y1 = int(xs.min().item()), int(ys.min().item())
        x2, y2 = int(xs.max().item()), int(ys.max().item())
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(orig_w, x2), min(orig_h, y2)
        if x2 <= x1 or y2 <= y1:
            continue

        crop = image.crop((x1, y1, x2, y2))
        rec_inputs = rec_proc(images=crop, return_tensors="pt")
        rec_inputs = {k: v.to(device) for k, v in rec_inputs.items()}

        with torch.no_grad():
            rec_outputs = rec_model(**rec_inputs)

        rec_results = rec_proc.post_process_text_recognition(rec_outputs)
        text = rec_results[0]["text"]
        score = rec_results[0]["score"]

        detections.append({
            "text": text,
            "confidence": round(float(score), 4),
            "det_score": round(float(det_scores[i].item()), 4),
            "bbox_xyxy": [x1, y1, x2, y2],
        })

    elapsed = time.perf_counter() - t0
    print(f"      {len(polygons)} boxes detected → {len(detections)} text regions  ({elapsed:.1f}s)")
    detections.sort(key=lambda d: (d["bbox_xyxy"][1], d["bbox_xyxy"][0]))
    return detections


def print_summary(detections: list[dict], image_name: str) -> None:
    print(f"\n{'─' * 70}")
    print(f"  PP-OCRv5  →  {image_name}")
    print(f"  Text regions: {len(detections)}")
    print(f"{'─' * 70}")
    for i, det in enumerate(detections, 1):
        text_preview = det["text"][:50] + ("…" if len(det["text"]) > 50 else "")
        x1, y1, x2, y2 = det["bbox_xyxy"]
        print(f"  [{i:02d}] conf={det['confidence']:.3f}  ({x1},{y1})→({x2},{y2})  {text_preview}")
    print(f"{'─' * 70}\n")


def save_outputs(detections: list[dict], image_path: Path, output_dir: Path, save_json: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_path.stem

    txt_out = output_dir / f"{stem}_ocr.txt"
    txt_out.write_text("\n".join(d["text"] for d in detections), encoding="utf-8")
    print(f"[3/3] OCR text saved  →  {txt_out}")

    if save_json:
        json_out = output_dir / f"{stem}_detections.json"
        payload = {"image": str(image_path), "total_regions": len(detections), "detections": detections}
        json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"      JSON saved  →  {json_out}")


def main() -> None:
    args = build_parser().parse_args()
    image_path = Path(args.image).resolve()
    if not image_path.exists():
        sys.exit(f"[ERROR] Image not found: {image_path}")

    device = resolve_device(args.device)
    det_bundle, rec_bundle = load_models(device)
    detections = run_inference(det_bundle, rec_bundle, image_path, device)
    print_summary(detections, image_path.name)
    save_outputs(detections, image_path, Path(args.output_dir), args.save_json)

    if not detections:
        print("[WARN] No text detected")


if __name__ == "__main__":
    main()
