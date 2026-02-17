#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:."
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
if [[ -z "${TEST_DATABASE_URL:-}" ]]; then
  export TEST_DATABASE_URL="$(
    python3 -c "import os; from app.db.config import build_database_url; os.environ['POSTGRES_DB']=os.getenv('POSTGRES_TEST_DB','jfb_docs_test'); print(build_database_url())"
  )"
fi
python3 -m pytest
