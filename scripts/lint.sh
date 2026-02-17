#!/usr/bin/env bash
set -euo pipefail

if python3 -m ruff --version >/dev/null 2>&1; then
  python3 -m ruff check app tests
else
  echo "ruff is not installed. Run: make install"
  exit 1
fi
