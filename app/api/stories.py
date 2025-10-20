from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ..db.session import get_db
from ..domain.story.schemas import CreateStory, StoryOut, CreateChapter, ChapterOut
from ..domain.story import service as story_service

router = APIRouter(prefix="/stories", tags=["stories"])


@router.post("/", response_model=StoryOut)
async def create_story(data: CreateStory, db: AsyncSession = Depends(get_db)):
    story = await story_service.create_story(db, data, owner_id=None)
    return story


@router.get("/{story_id}", response_model=StoryOut)
async def get_story(story_id: UUID, db: AsyncSession = Depends(get_db)):
    story = await story_service.get_story(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story


@router.post("/{story_id}/chapters", response_model=ChapterOut)
async def create_chapter(story_id: UUID, data: CreateChapter, db: AsyncSession = Depends(get_db)):
    chapter = await story_service.create_chapter(db, data)
    return chapter


@router.get("/{story_id}/chapters", response_model=list[ChapterOut])
async def list_chapters(story_id: UUID, db: AsyncSession = Depends(get_db)):
    chapters = await story_service.list_chapters(db, story_id)
    return chapters


@router.get("/{story_id}/chapters/search", response_model=list[ChapterOut])
async def search_chapters(story_id: UUID, q: str, k: int = 3, db: AsyncSession = Depends(get_db)):
    from ..domain.story.embedding import embed

    vec = await embed(q)
    chapters = await story_service.search_chapters(db, story_id, vec, k)
    return chapters
