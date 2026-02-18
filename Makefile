.PHONY: install dev test test-db lint discover-urls db-up db-down migrate-up migrate-down db-reset

install:
	python3 -m pip install -e .[dev]

dev:
	./scripts/dev.sh

test:
	./scripts/test.sh

test-db: db-up
	ALLOW_DESTRUCTIVE_TEST_DB_RESET=1 ./scripts/test.sh

lint:
	./scripts/lint.sh

discover-urls:
	bash ./scripts/discover_urls.sh

db-up:
	docker compose up -d db
	docker compose exec -T db sh -c "retries=30; until pg_isready -U $${POSTGRES_USER:-jfb_user} -d postgres; do retries=$$((retries - 1)); if [ $$retries -le 0 ]; then echo 'Postgres did not become ready within 30s' >&2; exit 1; fi; sleep 1; done"
	docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "SELECT 1 FROM pg_database WHERE datname='$${POSTGRES_TEST_DB:-jfb_docs_test}'" | grep -q 1 || docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "CREATE DATABASE $${POSTGRES_TEST_DB:-jfb_docs_test}"

db-down:
	docker compose down

migrate-up:
	python3 -m alembic upgrade head

migrate-down:
	python3 -m alembic downgrade -1

db-reset:
	@db_host="$${POSTGRES_HOST:-localhost}"; \
	case "$$db_host" in \
	localhost|127.0.0.1|::1) ;; \
	*) echo "Refusing db-reset for non-local POSTGRES_HOST=$$db_host"; exit 1 ;; \
	esac
	docker compose down -v
	docker compose up -d db
	docker compose exec -T db sh -c "retries=30; until pg_isready -U $${POSTGRES_USER:-jfb_user} -d postgres; do retries=$$((retries - 1)); if [ $$retries -le 0 ]; then echo 'Postgres did not become ready within 30s' >&2; exit 1; fi; sleep 1; done"
	docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "SELECT 1 FROM pg_database WHERE datname='$${POSTGRES_TEST_DB:-jfb_docs_test}'" | grep -q 1 || docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "CREATE DATABASE $${POSTGRES_TEST_DB:-jfb_docs_test}"
	DATABASE_URL="$$(python3 -c "import os; from app.db.config import build_database_url; os.environ['POSTGRES_DB']=os.getenv('POSTGRES_DB','jfb_docs'); print(build_database_url())")" python3 -m alembic upgrade head
	DATABASE_URL="$$(python3 -c "import os; from app.db.config import build_database_url; os.environ['POSTGRES_DB']=os.getenv('POSTGRES_TEST_DB','jfb_docs_test'); print(build_database_url())")" python3 -m alembic upgrade head
