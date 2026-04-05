#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "══════════════════════════════════════════════════"
echo " GOT-OCR2.0 POC"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════"

uv sync --no-progress --reinstall-package torch --reinstall-package torchvision
uv run python generate_sample.py
uv run python poc_runner.py --image sample_outputs/sample_doc.png --save-json
