#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "══════════════════════════════════════════════════"
echo " PaddleOCR v5 POC"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════"

uv sync --no-progress
uv run python generate_sample.py
uv run python poc_runner.py --image sample_outputs/sample_doc.png --save-json
