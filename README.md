# Quantum Writer

Monolithic FastAPI application for AI-powered storytelling.

## Quick Start

```bash
cp .env.example .env
poetry install --with dev
make init-db
make dev
```

The API will be available at http://localhost:8000

## Make Targets

- `make dev` - start dev server
- `make init-db` - create database and run migrations
- `make lint` - run ruff
- `make test` - run tests
- `make down` - stop dev server
- `make clean` - remove cache
