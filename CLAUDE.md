# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Quantum Writer v2 is a microservices-based AI-powered storytelling platform using:
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI microservices (Python 3.11+)
- **Databases**: PostgreSQL, Redis, Qdrant, Elasticsearch
- **AI**: Multi-model support (Claude, GPT-4, Llama)

## Essential Commands

```bash
# Development
make setup    # Initial setup (run once)
make dev      # Start all services
make stop     # Stop services
make ps       # Check service status
make logs     # View logs

# Testing & Quality
make test     # Run all tests
make lint     # Lint all code

# Database
make migrate  # Run migrations

# Cleanup
make clean    # Remove containers/volumes
```

## Service Architecture

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Next.js UI |
| API Gateway | 8000 | Kong routing |
| Story Service | 8010 | Story/chapter CRUD |
| AI Service | 8011 | LLM integration |
| Analysis Service | 8012 | NLP analysis |
| Context Service | 8013 | Vector search |
| Auth Service | 8014 | Authentication |
| WebSocket Service | 8015 | Real-time sync |

## Key Development Patterns

1. **API Structure**: All services follow `/api/v1/{resource}` pattern with FastAPI
2. **Database Models**: SQLAlchemy models in `services/{service}/app/models/`
3. **Frontend Components**: React components in `frontend/src/components/` using Shadcn/ui
4. **Environment**: Copy `.env.example` to `.env` before starting

## Important Context Files
- `context/` directory contains story examples and narrative artifacts
- Each service has its own `requirements.txt` and Dockerfile
- Database migrations use Alembic in each service

## Common Tasks

**Adding a new API endpoint:**
1. Define model in `services/{service}/app/models/`
2. Create schema in `services/{service}/app/schemas/`
3. Add route in `services/{service}/app/api/v1/`

**Frontend development:**
- Components use TypeScript and Tailwind CSS
- API calls through `/api` proxy to gateway
- State management with React hooks

**Testing:**
- Backend: pytest in each service directory
- Frontend: Jest tests in `frontend/`