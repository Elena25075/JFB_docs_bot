#!/usr/bin/env bash
set -euo pipefail

if command -v ruff >/dev/null 2>&1; then
  ruff check .
else
  echo "ruff is not installed. Run: make install"
  exit 1
fi
