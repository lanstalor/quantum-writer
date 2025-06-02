from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from typing import List, Optional
import uuid
import httpx

from app.models.chapter import Chapter
from app.models.story import Story
from app.schemas.chapter import ChapterCreate, ChapterUpdate, GenerateChapterRequest

class ChapterService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_chapter(self, chapter_data: ChapterCreate) -> Chapter:
        """Create a new chapter"""
        # Calculate position if not provided
        if chapter_data.position is None:
            result = await self.db.execute(
                select(func.max(Chapter.position))
                .where(Chapter.story_id == chapter_data.story_id)
            )
            max_position = result.scalar()
            chapter_data.position = (max_position or 0) + 1
        
        # Calculate word count
        word_count = len(chapter_data.content.split()) if chapter_data.content else 0
        
        chapter = Chapter(
            id=str(uuid.uuid4()),
            story_id=chapter_data.story_id,
            branch_id=chapter_data.branch_id,
            title=chapter_data.title,
            content=chapter_data.content,
            position=chapter_data.position,
            word_count=word_count
        )
        
        self.db.add(chapter)
        await self.db.commit()
        await self.db.refresh(chapter)
        return chapter
    
    async def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """Get a chapter by ID"""
        result = await self.db.execute(
            select(Chapter).where(Chapter.id == chapter_id)
        )
        return result.scalar_one_or_none()
    
    async def get_chapters_by_story(self, story_id: str) -> List[Chapter]:
        """Get all chapters for a story, ordered by position"""
        result = await self.db.execute(
            select(Chapter)
            .where(Chapter.story_id == story_id)
            .order_by(Chapter.position)
        )
        return list(result.scalars().all())
    
    async def update_chapter(self, chapter_id: str, chapter_data: ChapterUpdate) -> Optional[Chapter]:
        """Update a chapter"""
        chapter = await self.get_chapter(chapter_id)
        if not chapter:
            return None
        
        update_data = chapter_data.model_dump(exclude_unset=True)
        
        # Recalculate word count if content is updated
        if 'content' in update_data:
            update_data['word_count'] = len(update_data['content'].split())
        
        if update_data:
            await self.db.execute(
                update(Chapter)
                .where(Chapter.id == chapter_id)
                .values(**update_data)
            )
            await self.db.commit()
            await self.db.refresh(chapter)
        
        return chapter
    
    async def delete_chapter(self, chapter_id: str) -> bool:
        """Delete a chapter"""
        result = await self.db.execute(
            delete(Chapter).where(Chapter.id == chapter_id)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def reorder_chapters(self, story_id: str, chapter_positions: dict) -> bool:
        """Reorder chapters in a story"""
        try:
            for chapter_id, position in chapter_positions.items():
                await self.db.execute(
                    update(Chapter)
                    .where(Chapter.id == chapter_id, Chapter.story_id == story_id)
                    .values(position=position)
                )
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            return False
    
    async def generate_chapter_with_ai(self, request: GenerateChapterRequest) -> Chapter:
        """Generate a new chapter using AI service"""
        # Get story context for AI generation
        chapters = await self.get_chapters_by_story(request.story_id)
        context = ""
        
        if chapters:
            # Build context from previous chapters
            context_parts = []
            for chapter in chapters[-3:]:  # Use last 3 chapters for context
                context_parts.append(f"Chapter {chapter.position}: {chapter.title}\n{chapter.content}")
            context = "\n\n".join(context_parts)
        
        # Call AI service
        ai_url = "http://ai-service:8000/api/v1/generate"  # Internal docker network
        ai_request = {
            "prompt": request.prompt,
            "context": context,
            "system_prompt": request.system_prompt or "You are a creative writing assistant continuing a story. Maintain consistency with the existing narrative and characters."
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(ai_url, json=ai_request, timeout=60.0)
                response.raise_for_status()
                ai_response = response.json()
                generated_content = ai_response.get("content", "")
        except Exception as e:
            raise Exception(f"Failed to generate content with AI: {str(e)}")
        
        # Create chapter with generated content
        chapter_data = ChapterCreate(
            story_id=request.story_id,
            title=request.title,
            content=generated_content,
            position=request.position
        )
        
        return await self.create_chapter(chapter_data)