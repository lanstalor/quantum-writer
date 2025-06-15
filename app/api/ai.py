from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..core.ai_registry import registry

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate")
async def generate(prompt: str, model: str = "groq"):
    adapter = registry.get(model)
    if not adapter:
        raise HTTPException(status_code=400, detail="model not found")

    async def streamer():
        async for token in adapter.generate(prompt):
            yield token + " "

    return StreamingResponse(streamer(), media_type="text/plain")
