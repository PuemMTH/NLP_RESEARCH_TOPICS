"""
WangchanBERTa MLM — OCR Post-Correction POC
=============================================
Stage 4: Post-correction (masked language model approach).

Uses WangchanBERTa (Thai BERT by VISTEC/AIResearch) for context-aware
token prediction. The MLM head predicts the most likely token at masked
positions — useful for correcting OCR errors where the surrounding
context is intact.

Approach:
  1. Identify low-confidence OCR tokens (from Stage 3 output)
  2. Replace them with <mask>
  3. Use WangchanBERTa MLM to predict the correct token
  4. Accept prediction if confidence exceeds threshold

Usage:
  uv run python poc_runner.py --input sample_outputs/sample_masked_texts.json
  uv run python poc_runner.py --text "ผู้ป่วยมาด้วย<mask>ปวดท้อง" --save-json
"""

import argparse
import json
import sys
import time
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="WangchanBERTa MLM OCR post-correction POC")
    p.add_argument("--input", help="JSON file with masked texts")
    p.add_argument("--text", help="Single masked text to fill")
    p.add_argument("--model-name", default="airesearch/wangchanberta-base-att-spm-uncased",
                   help="HuggingFace model ID")
    p.add_argument("--top-k", type=int, default=5, help="Number of top predictions per mask")
    p.add_argument("--device", default=None, help="Device: 'cuda', 'cpu', or None=auto")
    p.add_argument("--output-dir", default="sample_outputs", help="Output directory")
    p.add_argument("--save-json", action="store_true", help="Save predictions as JSON")
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
        from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline
    except ImportError:
        sys.exit("[ERROR] transformers not installed. Run: uv sync")

    print(f"[1/3] Loading WangchanBERTa  {model_name}  …")
    fill_pipe = pipeline("fill-mask", model=model_name, device=device, top_k=10)
    print(f"      Model loaded.")
    return fill_pipe


def predict_masks(fill_pipe, text: str, top_k: int) -> list[dict]:
    """Run fill-mask pipeline on text containing <mask> tokens."""
    # WangchanBERTa uses <mask> token
    mask_token = fill_pipe.tokenizer.mask_token
    # Replace <mask> with the model's actual mask token if different
    query = text.replace("<mask>", mask_token)

    results = fill_pipe(query, top_k=top_k)

    # fill-mask returns list of dicts (single mask) or list of lists (multi mask)
    if results and isinstance(results[0], dict):
        results = [results]  # wrap single mask result

    predictions = []
    for mask_idx, preds in enumerate(results):
        top_preds = []
        for pred in preds[:top_k]:
            top_preds.append({
                "token": pred["token_str"].strip(),
                "score": round(pred["score"], 4),
            })
        predictions.append({
            "mask_index": mask_idx,
            "top_predictions": top_preds,
            "best": top_preds[0]["token"] if top_preds else "",
            "best_score": top_preds[0]["score"] if top_preds else 0.0,
        })

    return predictions


def run_batch(fill_pipe, samples: list[dict], top_k: int) -> list[dict]:
    results = []
    for i, sample in enumerate(samples, 1):
        masked_text = sample.get("masked", sample.get("text", ""))
        expected = sample.get("expected_fill", "")
        context = sample.get("context", "")

        t0 = time.perf_counter()
        predictions = predict_masks(fill_pipe, masked_text, top_k)
        elapsed = time.perf_counter() - t0

        best = predictions[0]["best"] if predictions else ""
        results.append({
            "masked_text": masked_text,
            "expected": expected,
            "context": context,
            "predictions": predictions,
            "best_fill": best,
            "match": best.strip() == expected.strip() if expected else None,
            "time_s": round(elapsed, 3),
        })
    return results


def print_summary(results: list[dict]) -> None:
    print(f"\n{'─' * 80}")
    print(f"  WangchanBERTa MLM Fill-Mask  →  {len(results)} samples")
    print(f"{'─' * 80}")
    for i, r in enumerate(results, 1):
        status = "✓" if r.get("match") else "✗" if r.get("match") is False else "?"
        print(f"\n  [{i:02d}] {status}  {r['time_s']:.3f}s  ({r.get('context', '')})")
        print(f"    masked:   {r['masked_text'][:70]}")
        if r["predictions"]:
            preds = r["predictions"][0]
            top3 = ", ".join(f"{p['token']}({p['score']:.3f})" for p in preds["top_predictions"][:3])
            print(f"    top-3:    {top3}")
        if r["expected"]:
            print(f"    expected: {r['expected']}")
        print(f"    best:     {r['best_fill']}")

    if any(r.get("match") is not None for r in results):
        matches = sum(1 for r in results if r.get("match"))
        total = sum(1 for r in results if r.get("match") is not None)
        print(f"\n  Exact-match accuracy: {matches}/{total} ({matches/total*100:.0f}%)")
    print(f"{'─' * 80}\n")


def save_outputs(results: list[dict], output_dir: Path, save_json: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    txt_out = output_dir / "mlm_predictions.txt"
    lines = []
    for r in results:
        lines.append(f"MASKED: {r['masked_text']}")
        lines.append(f"BEST:   {r['best_fill']}")
        if r["expected"]:
            lines.append(f"EXPECT: {r['expected']}")
        lines.append("")
    txt_out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[3/3] Predictions saved  →  {txt_out}")

    if save_json:
        json_out = output_dir / "mlm_predictions.json"
        json_out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
        print(f"      JSON saved  →  {json_out}")


def main() -> None:
    args = build_parser().parse_args()

    if not args.input and not args.text:
        sys.exit("[ERROR] Provide --input (JSON file) or --text (single masked string)")

    device = resolve_device(args.device)
    fill_pipe = load_model(args.model_name, device)

    if args.text:
        samples = [{"masked": args.text, "expected_fill": "", "context": "CLI input"}]
    else:
        input_path = Path(args.input).resolve()
        if not input_path.exists():
            sys.exit(f"[ERROR] Input file not found: {input_path}")
        samples = json.loads(input_path.read_text(encoding="utf-8"))

    print(f"[2/3] Predicting masks for {len(samples)} samples …")
    results = run_batch(fill_pipe, samples, args.top_k)
    print_summary(results)
    save_outputs(results, Path(args.output_dir), args.save_json)


if __name__ == "__main__":
    main()
