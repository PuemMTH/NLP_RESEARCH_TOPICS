# VLM Zero-Shot Image Classifier POC

Replaces the hardcoded 700-character text-length OCR threshold (used to label SME product
images as "ad/label" vs "product") with a Vision-Language Model zero-shot classifier.

## Problem

Current system:
- Run OCR on image → count extracted characters
- If chars > 700 → classify as "advertisement/label image"
- Else → classify as "product image"

Weakness: brittle (depends on OCR quality), language-agnostic, ignores visual layout.

## Solution

Pass the image directly to a VLM with a structured prompt. The model returns:

```json
{
  "label": "product",
  "confidence": 0.92,
  "reasoning": "The image shows a single product bottle with minimal text on the label."
}
```

If `confidence < 0.7` → fall back to the 700-char rule (requires sidecar char count from OCR).

## Models

| Model | Notes |
|---|---|
| `scb10x/typhoon2-qwen2vl-7b-vision-instruct` | Primary — Thai-optimised Qwen2-VL-7B fine-tune |
| `Qwen/Qwen2.5-VL-7B-Instruct` | Fallback — strong multilingual baseline |

Both use `Qwen2VLForConditionalGeneration` (Typhoon2) or `Qwen2_5_VLForConditionalGeneration`
(Qwen2.5) — the runner branches automatically on the model ID.

## Pipeline Stage

```
Stage 2: Layout Detection  ← THIS POC
         ↓ "product"      → lightweight OCR / metadata only
         ↓ "advertisement" → full text-extraction pipeline (PaddleOCR, GOT-OCR)
```

## Setup

```bash
# Requires uv — https://docs.astral.sh/uv/
bash poc/vlm-zero-shot-classifier/run.sh
```

Or step by step:

```bash
cd poc/vlm-zero-shot-classifier/
uv sync
uv run python generate_sample.py
uv run python poc_runner.py --image sample_outputs/sample_product.png --save-json
uv run python poc_runner.py --image sample_outputs/sample_ad_label.png --save-json
```

## CLI Options

```
--image                  Path to input image (required)
--model-id               HuggingFace model ID (default: scb10x/typhoon2-qwen2vl-7b-vision-instruct)
--device                 'cuda' or 'cpu' (default: auto-detect)
--load-4bit              Load in 4-bit via bitsandbytes (~8 GB VRAM instead of ~15 GB)
--confidence-threshold   Float; below this → fallback to 700-char rule (default: 0.7)
--char-threshold         Integer; OCR char count threshold for legacy rule (default: 700)
--metadata-json          Path to sidecar JSON with char counts (default: auto-detected)
--max-new-tokens         Max tokens for VLM generation (default: 256)
--save-json              Save result to sample_outputs/<stem>_result.json
```

## VRAM Requirements

| Mode | VRAM |
|---|---|
| BF16 (default) | ~14–15 GB |
| 4-bit (`--load-4bit`) | ~6–8 GB |
| CPU (fallback) | RAM only; very slow |

If your GPU has < 15 GB VRAM, add `--load-4bit` to all commands.

## Output Format

The runner prints a comparison table to stdout:

```
================================================================
  VLM Zero-Shot Classifier — Result
================================================================
  Image        : sample_ad_label.png
  Model        : scb10x/typhoon2-qwen2vl-7b-vision-instruct
----------------------------------------------------------------
  VLM label    : advertisement    confidence=0.95
  Parse OK     : yes
  Reasoning    :
    The image contains large blocks of Thai promotional text,
    ingredient lists, and a barcode — consistent with a product
    label or advertisement flyer.
----------------------------------------------------------------
  700-char rule: advertisement    (char_count=843, threshold=700)
----------------------------------------------------------------
  Agreement    : AGREE
----------------------------------------------------------------
  Final label  : ADVERTISEMENT  (VLM decision, confidence sufficient)
================================================================
```

And optionally a JSON file at `sample_outputs/<stem>_result.json`.

## Thai Language Notes

- **Typhoon2-Vision** is explicitly fine-tuned for Thai image understanding — preferred for Thai medical/SME documents.
- **Qwen2.5-VL** has broad multilingual coverage but less Thai-specific tuning.
- Both models were NOT trained specifically on Thai medical document formats — monitor accuracy on clinical forms and adjust the confidence threshold as needed.
- For production: consider fine-tuning on a labelled set of Thai SME product images vs. ad flyers.

## Confidence Note

The VLM "confidence" is self-reported (the model is prompted to provide it). It is NOT a
calibrated probability. Treat the 0.7 threshold as a tunable heuristic and evaluate it on
your labelled dataset before deploying.

## Model Weight Caching

Weights are cached by HuggingFace hub at `~/.cache/huggingface/hub/` (default). Set
`HF_HOME` to relocate. The runner does NOT re-download on subsequent runs.

Do NOT commit model weights:
- `*.pt`, `*.safetensors`, `*.bin`, `*.onnx` are gitignored by convention.
- `sample_outputs/` contents (except `.gitkeep`) are gitignored.
