#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="/home/linuxbrew/.linuxbrew/bin/python3"

cd "$ROOT"
exec "$PYTHON" scripts/collect_online.py \
  --interval 1800 \
  --batch 30 \
  --new-kanji 10 \
  --max-words 10 \
  --max-word-length 6
