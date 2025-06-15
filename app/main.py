from fastapi import FastAPI
from .core.config import get_settings
from .api.stories import router as stories_router
from .api.ai import router as ai_router
from .api.auth import router as auth_router

app = FastAPI(title="Quantum Writer")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def load_settings():
    get_settings()

app.include_router(stories_router)
app.include_router(ai_router)
app.include_router(auth_router)
