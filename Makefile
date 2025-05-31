.PHONY: help dev stop build test lint clean migrate setup

help:
	@echo "Available commands:"
	@echo "  make setup    - Initial project setup"
	@echo "  make dev      - Start development environment"
	@echo "  make stop     - Stop all services"
	@echo "  make build    - Build all services"
	@echo "  make test     - Run all tests"
	@echo "  make lint     - Lint all code"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make migrate  - Run database migrations"

setup:
	@echo "Setting up development environment..."
	cp .env.example .env
	docker-compose build
	make migrate
	cd frontend && npm install
	@echo "Setup complete! Run 'make dev' to start."

dev:
	@echo "Starting development environment..."
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "API Gateway: http://localhost:8000"
	@echo "PgAdmin: http://localhost:5050"

stop:
	@echo "Stopping all services..."
	docker-compose down

build:
	@echo "Building all services..."
	docker-compose build --parallel

test:
	@echo "Running tests..."
	docker-compose run --rm story-service pytest
	docker-compose run --rm ai-service pytest
	docker-compose run --rm analysis-service pytest
	docker-compose run --rm context-service pytest
	docker-compose run --rm auth-service pytest
	cd frontend && npm test

lint:
	@echo "Linting code..."
	docker-compose run --rm story-service ruff check .
	docker-compose run --rm ai-service ruff check .
	docker-compose run --rm analysis-service ruff check .
	docker-compose run --rm context-service ruff check .
	docker-compose run --rm auth-service ruff check .
	cd frontend && npm run lint

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	docker system prune -f

migrate:
	@echo "Running database migrations..."
	docker-compose run --rm story-service alembic upgrade head

logs:
	docker-compose logs -f

ps:
	docker-compose ps