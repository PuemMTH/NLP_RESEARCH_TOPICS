#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "══════════════════════════════════════════════════"
echo " EasyOCR Thai+EN POC"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════"

uv sync --no-progress --reinstall-package torch --reinstall-package torchvision
uv run python generate_sample.py
uv run python poc_runner.py --image sample_outputs/sample_doc.png --save-json

echo ""
echo "══════════════════════════════════════════════════"
echo " Done!  outputs:"
echo "   OCR text       → sample_outputs/sample_doc_ocr.txt"
echo "   detections JSON → sample_outputs/sample_doc_detections.json"
echo "══════════════════════════════════════════════════"
