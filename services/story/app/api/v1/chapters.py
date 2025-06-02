from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.services.chapter_service import ChapterService
from app.schemas.chapter import (
    ChapterCreate, ChapterUpdate, ChapterResponse, 
    ChapterListResponse, GenerateChapterRequest
)

router = APIRouter()

@router.post("/", response_model=ChapterResponse)
async def create_chapter(
    chapter_data: ChapterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new chapter"""
    service = ChapterService(db)
    chapter = await service.create_chapter(chapter_data)
    return chapter

@router.get("/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(
    chapter_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a chapter by ID"""
    service = ChapterService(db)
    chapter = await service.get_chapter(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.put("/{chapter_id}", response_model=ChapterResponse)
async def update_chapter(
    chapter_id: str,
    chapter_data: ChapterUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a chapter"""
    service = ChapterService(db)
    chapter = await service.update_chapter(chapter_id, chapter_data)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.delete("/{chapter_id}")
async def delete_chapter(
    chapter_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a chapter"""
    service = ChapterService(db)
    success = await service.delete_chapter(chapter_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"message": "Chapter deleted successfully"}

@router.get("/story/{story_id}", response_model=List[ChapterListResponse])
async def get_story_chapters(
    story_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get all chapters for a story"""
    service = ChapterService(db)
    chapters = await service.get_chapters_by_story(story_id)
    return chapters

@router.post("/generate", response_model=ChapterResponse)
async def generate_chapter(
    request: GenerateChapterRequest,
    model: str = Query("groq", description="AI model to use: claude, groq, gpt"),
    db: AsyncSession = Depends(get_db)
):
    """Generate a new chapter using AI"""
    service = ChapterService(db)
    try:
        chapter = await service.generate_chapter_with_ai(request, model=model)
        return chapter
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/story/{story_id}/reorder")
async def reorder_chapters(
    story_id: str,
    chapter_positions: dict,
    db: AsyncSession = Depends(get_db)
):
    """Reorder chapters in a story"""
    service = ChapterService(db)
    success = await service.reorder_chapters(story_id, chapter_positions)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to reorder chapters")
    return {"message": "Chapters reordered successfully"}