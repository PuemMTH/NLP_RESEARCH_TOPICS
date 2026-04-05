#!/usr/bin/env bash
# ============================================================
# DocLayout-YOLO POC — end-to-end runner (uv)
#
# Usage:
#   bash poc/doclayout-yolo/run.sh           # from repo root
#   bash run.sh                              # from this folder
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "══════════════════════════════════════════════════"
echo " DocLayout-YOLO POC"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════"

# ── 1. Check uv is available ───────────────────────────────
if ! command -v uv &>/dev/null; then
    echo "[ERROR] uv not found. Install with:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi
echo "[1/4] uv $(uv --version)"

# ── 2. Sync dependencies ───────────────────────────────────
echo ""
echo "[2/4] Installing dependencies (uv sync) …"
# --reinstall-package torch/torchvision ensures the correct CUDA build is used
# when the index was changed (e.g. cu124 → cu128 for Blackwell GPUs)
uv sync --no-progress --reinstall-package torch --reinstall-package torchvision

# ── 3. Generate sample document image ─────────────────────
SAMPLE="image.png"
echo ""
echo "[3/4] Generating synthetic document image …"
uv run python generate_sample.py

# ── 4. Run layout detection ────────────────────────────────
echo ""
echo "[4/4] Running DocLayout-YOLO inference …"
uv run python poc_runner.py \
    --image "$SAMPLE" \
    --conf 0.2 \
    --imgsz 1024 \
    --output-dir sample_outputs \
    --save-json

echo ""
echo "══════════════════════════════════════════════════"
echo " Done!  outputs:"
echo "   annotated image → sample_outputs/sample_doc_annotated.png"
echo "   detections JSON → sample_outputs/sample_doc_detections.json"
echo "══════════════════════════════════════════════════"
