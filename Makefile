.PHONY: dev prod down down-dev down-prod build-dev build-prod logs migrate makemigrations shell-backend shell-frontend

# Development
dev:
	docker compose -f docker-compose.dev.yml up --build

dev-d:
	docker compose -f docker-compose.dev.yml up --build -d

build-dev:
	docker compose -f docker-compose.dev.yml build

down-dev:
	docker compose -f docker-compose.dev.yml down

# Production
prod:
	docker compose -f docker-compose.prod.yml up --build -d

build-prod:
	docker compose -f docker-compose.prod.yml build

down-prod:
	docker compose -f docker-compose.prod.yml down

# General
down:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.prod.yml down

logs:
	docker compose -f docker-compose.dev.yml logs -f

logs-backend:
	docker compose -f docker-compose.dev.yml logs -f backend

logs-frontend:
	docker compose -f docker-compose.dev.yml logs -f frontend

# Database & Migrations
migrate:
	docker compose -f docker-compose.dev.yml exec backend uv run alembic upgrade head

makemigrations:
	docker compose -f docker-compose.dev.yml exec backend uv run alembic revision --autogenerate -m "$(msg)"

# Shell access
shell-backend:
	docker compose -f docker-compose.dev.yml exec backend bash

shell-frontend:
	docker compose -f docker-compose.dev.yml exec frontend sh

shell-db:
	docker compose -f docker-compose.dev.yml exec db psql -U thermodyne -d thermodyne_crm

# Cleanup
clean:
	docker compose -f docker-compose.dev.yml down -v --rmi local
	docker compose -f docker-compose.prod.yml down -v --rmi local
