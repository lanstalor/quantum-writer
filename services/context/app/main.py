from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core import settings
from app.db.database import engine, Base, get_db
from app.models import StoryContext
from app.schemas import ContextCreate, ContextResponse

def summarize_content(content: str, max_tokens: int) -> str:
    """Naive summarization to keep content within token limits."""
    estimated_tokens = int(len(content.split()) * 1.3)
    if estimated_tokens <= max_tokens:
        return content

    sections = content.split("\n\n")
    preserved = "\n\n".join(sections[-30:])
    summary = (
        "STORY SUMMARY (TRUNCATED):\n[Summary would be generated here]\n\n" 
        "RECENT CONTENT:\n" + preserved
    )
    return summary

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="Quantum Writer Context Service", version="2.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}


@app.post("/api/v1/context/{story_id}", response_model=ContextResponse)
async def save_context(
    story_id: str,
    context: ContextCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(StoryContext).where(StoryContext.story_id == story_id))
    ctx = result.scalar_one_or_none()

    if ctx:
        new_content = ctx.content + "\n\n" + context.content
        ctx.content = summarize_content(new_content, settings.MAX_CONTEXT_TOKENS)
    else:
        ctx = StoryContext(
            story_id=story_id,
            content=summarize_content(context.content, settings.MAX_CONTEXT_TOKENS),
        )
        db.add(ctx)

    await db.commit()
    await db.refresh(ctx)
    return ctx


@app.get("/api/v1/context/{story_id}", response_model=ContextResponse)
async def get_context(
    story_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(StoryContext).where(StoryContext.story_id == story_id))
    ctx = result.scalar_one_or_none()
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    return ctx

