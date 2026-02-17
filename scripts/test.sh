#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:."
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python3 -m pytest
