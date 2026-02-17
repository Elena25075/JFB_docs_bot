.PHONY: install dev test lint db-up db-down

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
