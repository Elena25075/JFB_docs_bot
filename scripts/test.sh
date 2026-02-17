#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:."
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export TEST_DATABASE_URL="${TEST_DATABASE_URL:-postgresql+psycopg://jfb_user:jfb_password@localhost:5432/jfb_docs_test}"
python3 -m pytest
