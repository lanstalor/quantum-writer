from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.models.story import Story
from app.models.branch import Branch
from app.models.chapter import Chapter
from app.schemas.story import StoryCreate, StoryUpdate, StoryResponse
from app.core.security import get_current_user

router = APIRouter()



@router.post("/", response_model=StoryResponse)
async def create_story(
    story: StoryCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Create a new story"""
    import uuid
    
    story_id = str(uuid.uuid4())
    db_story = Story(
        id=story_id,
        **story.model_dump(),
        user_id=user_id
    )
    db.add(db_story)
    
    # Create main branch
    main_branch = Branch(
        id=str(uuid.uuid4()),
        story_id=story_id,
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


@router.get("/{story_id}/export")
async def export_story(
    story_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """Export a story and its chapters as Markdown"""
    result = await db.execute(
        select(Story).where(Story.id == story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    chapters_result = await db.execute(
        select(Chapter)
        .where(Chapter.story_id == story_id)
        .order_by(Chapter.position)
    )
    chapters = chapters_result.scalars().all()

    md_parts = [f"# {story.title}\n"]
    if story.description:
        md_parts.append(f"{story.description}\n")

    for chapter in chapters:
        md_parts.append(f"## Chapter {chapter.position}: {chapter.title}\n")
        md_parts.append(chapter.content + "\n")

    markdown = "\n".join(md_parts)

    headers = {
        "Content-Disposition": f"attachment; filename={story.title.replace(' ', '_')}.md"
    }
    return Response(content=markdown, media_type="text/markdown", headers=headers)
