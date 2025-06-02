from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core import settings
from app.api.v1.generate import router as generate_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Quantum Writer AI Service", version="2.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Include routers
app.include_router(generate_router, prefix="/api/v1", tags=["generation"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}

