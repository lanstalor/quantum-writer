.PHONY: dev init-db lint test down clean

dev:
uvicorn app.main:app --reload --port 8000

init-db:
alembic revision --autogenerate -m init && alembic upgrade head

lint:
ruff app

test:
pytest -q

down:
pkill -f uvicorn || true

clean:
rm -rf __pycache__ */__pycache__
