#!/usr/bin/env bash
# run.sh — End-to-end POC runner for vlm-zero-shot-classifier
# Usage: bash run.sh
#        bash run.sh --model-id Qwen/Qwen2.5-VL-7B-Instruct
#        bash run.sh --load-4bit
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "  vlm-zero-shot-classifier POC"
echo "  $(date)"
echo "========================================================"

# Accept extra CLI args to forward to poc_runner.py (e.g. --load-4bit, --model-id)
EXTRA_ARGS=("$@")

# ------------------------------------------------------------------
# Step 1: Sync dependencies (cu128 PyTorch — supports Blackwell + older)
# ------------------------------------------------------------------
echo ""
echo "[1/4] Syncing dependencies via uv ..."
# --reinstall-package torch ensures the cu128 build is selected if index changed
uv sync --no-progress --reinstall-package torch --reinstall-package torchvision

# ------------------------------------------------------------------
# Step 2: Generate synthetic sample images + sidecar metadata
# ------------------------------------------------------------------
echo ""
echo "[2/4] Generating synthetic sample images ..."
uv run python generate_sample.py

# ------------------------------------------------------------------
# Step 3: Classify the product image
# ------------------------------------------------------------------
echo ""
echo "[3/4] Classifying product image ..."
uv run python poc_runner.py \
    --image sample_outputs/sample_product.png \
    --save-json \
    "${EXTRA_ARGS[@]}"

# ------------------------------------------------------------------
# Step 4: Classify the ad/label image
# ------------------------------------------------------------------
echo ""
echo "[4/4] Classifying ad/label image ..."
uv run python poc_runner.py \
    --image sample_outputs/sample_ad_label.png \
    --save-json \
    "${EXTRA_ARGS[@]}"

echo ""
echo "========================================================"
echo "  All done. Results in: $SCRIPT_DIR/sample_outputs/"
echo "========================================================"
