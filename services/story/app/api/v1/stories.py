from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.db.database import get_db
from app.models.story import Story
from app.models.branch import Branch
from app.schemas.story import StoryCreate, StoryUpdate, StoryResponse

router = APIRouter()


async def get_current_user(x_user_id: Optional[str] = Header(None)) -> str:
    """Simple auth dependency expecting an X-User-Id header."""
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing authentication")
    return x_user_id

@router.post("/", response_model=StoryResponse)
async def create_story(
    story: StoryCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Create a new story"""
    db_story = Story(
        **story.model_dump(),
        user_id=user_id
    )
    db.add(db_story)
    
    # Create main branch
    main_branch = Branch(
        story_id=db_story.id,
        name="main",
        description="Main storyline",
        is_main=True
    )
    db.add(main_branch)
    
    await db.commit()
    await db.refresh(db_story)
    
    return db_story

@router.get("/", response_model=List[StoryResponse])
async def list_stories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """List user's stories"""
    result = await db.execute(
        select(Story)
        .where(Story.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    stories = result.scalars().all()
    return stories

@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(
    story_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Get a specific story"""
    result = await db.execute(
        select(Story)
        .where(Story.id == story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    return story

@router.put("/{story_id}", response_model=StoryResponse)
async def update_story(
    story_id: str,
    story_update: StoryUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Update a story"""
    result = await db.execute(
        select(Story)
        .where(Story.id == story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    for field, value in story_update.model_dump(exclude_unset=True).items():
        setattr(story, field, value)
    
    await db.commit()
    await db.refresh(story)
    
    return story

@router.delete("/{story_id}")
async def delete_story(
    story_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Delete a story"""
    result = await db.execute(
        select(Story)
        .where(Story.id == story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()
    
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    await db.delete(story)
    await db.commit()
    
    return {"message": "Story deleted successfully"}