"""
DocLayout-YOLO — Proof of Concept Runner
=========================================
Model : juliozhao/DocLayout-YOLO-DocStructBench  (HuggingFace)
Source: https://github.com/opendatalab/DocLayout-YOLO

Detects the following layout classes in document images:
  0 title           1 plain text      2 abandon
  3 figure          4 figure_caption  5 table
  6 table_caption   7 table_footnote  8 isolate_formula
  9 formula_caption

Usage
-----
  python poc_runner.py --image path/to/doc.png
  python poc_runner.py --image path/to/doc.png --conf 0.3 --save-json
  python poc_runner.py --image path/to/doc.png --conf 0.3 --device cpu --save-json

Setup (uv)
----------
  uv sync
  uv run python poc_runner.py --image path/to/doc.png

Note on Thai medical documents
-------------------------------
  The model was trained mainly on English-heavy scholarly/PDF layouts.
  Results on Thai medical forms may vary; treat this run as a baseline
  before any domain-specific fine-tuning.
"""

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="DocLayout-YOLO POC — document layout detection"
    )
    p.add_argument(
        "--image", required=True,
        help="Path to an input document image (PNG / JPG / TIFF)"
    )
    p.add_argument(
        "--conf", type=float, default=0.2,
        help="Confidence threshold for detections (default: 0.2)"
    )
    p.add_argument(
        "--imgsz", type=int, default=1024,
        help="Inference image size in pixels (default: 1024)"
    )
    p.add_argument(
        "--device", default=None,
        help="Inference device: 'cpu' or '0' for first GPU (default: auto — uses CUDA if available)"
    )
    p.add_argument(
        "--output-dir", default="sample_outputs",
        help="Directory to write annotated image (default: sample_outputs)"
    )
    p.add_argument(
        "--save-json", action="store_true",
        help="Also write detections as a JSON file alongside the annotated image"
    )
    return p


# ---------------------------------------------------------------------------
# Device resolution — GPU first, CPU fallback
# ---------------------------------------------------------------------------

def resolve_device(requested: str | None) -> str:
    """Return the best available device string for YOLO.

    Priority: explicit arg > CUDA (first GPU) > CPU

    Also validates that the selected GPU's compute capability is supported
    by the installed PyTorch build.  RTX 50xx (Blackwell, sm_120) requires
    PyTorch built against CUDA 12.8+ (cu128 index).
    """
    import torch

    if requested is not None:
        device = requested
        if device != "cpu" and not torch.cuda.is_available():
            print(f"[WARN] --device {device} requested but CUDA not available; falling back to cpu")
            device = "cpu"
    elif torch.cuda.is_available():
        device = "0"  # first GPU
    else:
        device = "cpu"

    if device != "cpu":
        props = torch.cuda.get_device_properties(int(device))
        sm_str = f"sm_{props.major}{props.minor}"
        arch_list = torch.cuda.get_arch_list()  # e.g. ['sm_50', ..., 'sm_90']

        if sm_str not in arch_list:
            print(f"[WARN] GPU {props.name} ({sm_str}) is NOT supported by this PyTorch build.")
            print(f"       Compiled for: {', '.join(arch_list)}")
            print(f"       Fix: change pyproject.toml index to pytorch-cu128, then run:")
            print(f"         uv sync --reinstall-package torch --reinstall-package torchvision")
            print(f"       Falling back to cpu for this run.")
            device = "cpu"
        else:
            vram = props.total_memory / 1024 ** 3
            print(f"[device] CUDA:{device}  {props.name}  ({sm_str})  ({vram:.1f} GB VRAM)")

    if device == "cpu":
        print("[device] cpu")

    return device


# ---------------------------------------------------------------------------
# Model loading (cached after first download)
# ---------------------------------------------------------------------------

def load_model(device: str):
    try:
        from huggingface_hub import hf_hub_download
        from doclayout_yolo import YOLOv10
    except ImportError as e:
        sys.exit(
            f"[ERROR] Missing dependency: {e}\n"
            "Run:  uv sync"
        )

    print("[1/3] Downloading / loading model weights from HuggingFace …")
    weights_path = hf_hub_download(
        repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
        filename="doclayout_yolo_docstructbench_imgsz1024.pt",
    )
    model = YOLOv10(weights_path)
    print(f"      Model loaded  →  {weights_path}")
    return model


# ---------------------------------------------------------------------------
# Class label map
# ---------------------------------------------------------------------------

LABEL_MAP = {
    0: "title",
    1: "plain_text",
    2: "abandon",
    3: "figure",
    4: "figure_caption",
    5: "table",
    6: "table_caption",
    7: "table_footnote",
    8: "isolate_formula",
    9: "formula_caption",
}


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def run_inference(model, image_path: Path, conf: float, imgsz: int, device: str):
    print(f"[2/3] Running inference on  {image_path.name}  …")
    results = model.predict(
        str(image_path),
        imgsz=imgsz,
        conf=conf,
        device=device,
    )
    return results


# ---------------------------------------------------------------------------
# Parse & display results
# ---------------------------------------------------------------------------

def parse_detections(result) -> list[dict]:
    detections = []
    if result.boxes is None:
        return detections

    for box in result.boxes:
        cls_id = int(box.cls.item())
        confidence = round(float(box.conf.item()), 4)
        x1, y1, x2, y2 = [round(v, 1) for v in box.xyxy[0].tolist()]
        detections.append(
            {
                "label": LABEL_MAP.get(cls_id, f"class_{cls_id}"),
                "class_id": cls_id,
                "confidence": confidence,
                "bbox_xyxy": [x1, y1, x2, y2],
            }
        )
    # Sort by y-coordinate (reading order approximation)
    detections.sort(key=lambda d: d["bbox_xyxy"][1])
    return detections


def print_summary(detections: list[dict], image_name: str) -> None:
    print(f"\n{'─'*60}")
    print(f"  DocLayout-YOLO  →  {image_name}")
    print(f"  Detections: {len(detections)}")
    print(f"{'─'*60}")

    # Count per label
    from collections import Counter
    counts = Counter(d["label"] for d in detections)
    for label, n in sorted(counts.items()):
        print(f"  {label:<20} {n:>3} region(s)")

    print(f"{'─'*60}")
    print("  Detailed  (sorted top→bottom by y1)")
    print(f"{'─'*60}")
    for i, det in enumerate(detections, 1):
        x1, y1, x2, y2 = det["bbox_xyxy"]
        print(
            f"  [{i:02d}] {det['label']:<20} "
            f"conf={det['confidence']:.3f}  "
            f"bbox=({x1:.0f},{y1:.0f})→({x2:.0f},{y2:.0f})"
        )
    print(f"{'─'*60}\n")


# ---------------------------------------------------------------------------
# Save outputs
# ---------------------------------------------------------------------------

def save_outputs(
    result,
    detections: list[dict],
    image_path: Path,
    output_dir: Path,
    save_json: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_path.stem

    # Annotated image
    annotated = result.plot(pil=True, line_width=3, font_size=16)
    img_out = output_dir / f"{stem}_annotated.png"
    # doclayout_yolo may return either PIL.Image or numpy.ndarray.
    if hasattr(annotated, "save"):
        annotated.save(str(img_out))
    else:
        from PIL import Image
        import numpy as np

        arr = np.asarray(annotated)
        if arr.ndim == 3 and arr.shape[2] == 3:
            # Ultralytics-style plot output is usually BGR ndarray.
            arr = arr[:, :, ::-1]
        Image.fromarray(arr).save(str(img_out))
    print(f"[3/3] Annotated image saved  →  {img_out}")

    # Optional JSON
    if save_json:
        json_out = output_dir / f"{stem}_detections.json"
        payload = {
            "image": str(image_path),
            "total_detections": len(detections),
            "detections": detections,
        }
        json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        print(f"      JSON detections saved  →  {json_out}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = build_parser().parse_args()
    image_path = Path(args.image).resolve()

    if not image_path.exists():
        sys.exit(f"[ERROR] Image not found: {image_path}")

    device = resolve_device(args.device)
    model = load_model(device)
    results = run_inference(model, image_path, args.conf, args.imgsz, device)

    all_detections: list[dict] = []
    for result in results:
        dets = parse_detections(result)
        all_detections.extend(dets)
        print_summary(dets, image_path.name)
        save_outputs(
            result,
            dets,
            image_path,
            Path(args.output_dir),
            args.save_json,
        )

    if not all_detections:
        print("[WARN] No regions detected — try lowering --conf")


if __name__ == "__main__":
    main()
