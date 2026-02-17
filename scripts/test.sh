#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-}:."
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
export TEST_DATABASE_URL="${TEST_DATABASE_URL:-postgresql+psycopg://${POSTGRES_USER:-jfb_user}:${POSTGRES_PASSWORD:-jfb_password}@${POSTGRES_HOST:-localhost}:${POSTGRES_PORT:-5432}/${POSTGRES_TEST_DB:-jfb_docs_test}}"
python3 -m pytest
