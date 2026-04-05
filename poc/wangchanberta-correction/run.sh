#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "══════════════════════════════════════════════════"
echo " WangchanBERTa MLM Post-Correction POC"
echo " $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════"

uv sync --no-progress --reinstall-package torch --reinstall-package torchvision
uv run python generate_sample.py
uv run python poc_runner.py --input sample_outputs/sample_masked_texts.json --save-json
