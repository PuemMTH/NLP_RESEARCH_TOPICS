#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [run.sh] Step 1: uv sync ==="
uv sync --no-progress --reinstall-package torch --reinstall-package torchvision

echo ""
echo "=== [run.sh] Step 2: generate sample test pairs ==="
uv run python generate_sample.py

echo ""
echo "=== [run.sh] Step 3: run single-pair demo ==="
uv run python poc_runner.py \
    --reference "ยาแก้ปวดหัว" \
    --hypothesis "ยาแกปวดหว"

echo ""
echo "=== [run.sh] Step 4: run full test suite (5 pairs) + save JSON ==="
uv run python poc_runner.py \
    --test-suite sample_outputs/test_pairs.json \
    --save-json sample_outputs/eval_results.json

echo ""
echo "=== [run.sh] Complete. Results in sample_outputs/ ==="
