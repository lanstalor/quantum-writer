from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core import settings
from pydantic import BaseModel
from app.services.analysis_engine import AnalysisEngine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(title="Quantum Writer Analysis Service", version="2.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}


class TextRequest(BaseModel):
    text: str


@app.post("/api/v1/analyze/characters")
async def analyze_characters(request: TextRequest):
    try:
        characters = AnalysisEngine.extract_characters(request.text)
        return {"characters": characters}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/analyze/plot")
async def analyze_plot(request: TextRequest):
    try:
        return AnalysisEngine.analyze_plot(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

