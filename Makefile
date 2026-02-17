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
