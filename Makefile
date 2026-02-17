.PHONY: install dev test test-db lint db-up db-down migrate-up migrate-down db-reset

install:
	python3 -m pip install -e .[dev]

dev:
	./scripts/dev.sh

test:
	./scripts/test.sh

test-db:
	ALLOW_DESTRUCTIVE_TEST_DB_RESET=1 ./scripts/test.sh

lint:
	./scripts/lint.sh

db-up:
	docker compose up -d db
	docker compose exec -T db sh -c "until pg_isready -U $${POSTGRES_USER:-jfb_user} -d postgres; do sleep 1; done"
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
	docker compose exec -T db sh -c "until pg_isready -U $${POSTGRES_USER:-jfb_user} -d postgres; do sleep 1; done"
	docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "SELECT 1 FROM pg_database WHERE datname='$${POSTGRES_TEST_DB:-jfb_docs_test}'" | grep -q 1 || docker compose exec -T db psql -U $${POSTGRES_USER:-jfb_user} -d postgres -c "CREATE DATABASE $${POSTGRES_TEST_DB:-jfb_docs_test}"
	DATABASE_URL="postgresql+psycopg://$${POSTGRES_USER:-jfb_user}:$${POSTGRES_PASSWORD:-jfb_password}@$${POSTGRES_HOST:-localhost}:$${POSTGRES_PORT:-5432}/$${POSTGRES_DB:-jfb_docs}" python3 -m alembic upgrade head
	TEST_DATABASE_URL="postgresql+psycopg://$${POSTGRES_USER:-jfb_user}:$${POSTGRES_PASSWORD:-jfb_password}@$${POSTGRES_HOST:-localhost}:$${POSTGRES_PORT:-5432}/$${POSTGRES_TEST_DB:-jfb_docs_test}" python3 -m alembic upgrade head
