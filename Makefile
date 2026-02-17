.PHONY: install dev test lint db-up db-down migrate-up migrate-down db-reset

install:
	python3 -m pip install -e .[dev]

dev:
	./scripts/dev.sh

test:
	./scripts/test.sh

lint:
	./scripts/lint.sh

db-up:
	docker compose up -d db
	docker compose exec -T db psql -U ${POSTGRES_USER:-jfb_user} -d postgres -c "SELECT 1 FROM pg_database WHERE datname='${POSTGRES_TEST_DB:-jfb_docs_test}'" | grep -q 1 || docker compose exec -T db psql -U ${POSTGRES_USER:-jfb_user} -d postgres -c "CREATE DATABASE ${POSTGRES_TEST_DB:-jfb_docs_test}"

db-down:
	docker compose down

migrate-up:
	python3 -m alembic upgrade head

migrate-down:
	python3 -m alembic downgrade -1

db-reset:
	docker compose down -v
	docker compose up -d db
	python3 -m alembic upgrade head
