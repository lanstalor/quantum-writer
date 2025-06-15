from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from .models import Story, Chapter
from .schemas import CreateStory, CreateChapter
from .embedding import embed


async def create_story(session: AsyncSession, data: CreateStory, owner_id: UUID | None) -> Story:
    story = Story(title=data.title, owner_id=owner_id)
    session.add(story)
    await session.commit()
    await session.refresh(story)
    return story


async def get_story(session: AsyncSession, story_id: UUID) -> Story | None:
    result = await session.execute(select(Story).where(Story.id == story_id))
    return result.scalar_one_or_none()


async def create_chapter(session: AsyncSession, data: CreateChapter) -> Chapter:
    vector = await embed(data.content)
    chapter = Chapter(story_id=data.story_id, title=data.title, content=data.content, embedding=vector)
    session.add(chapter)
    await session.commit()
    await session.refresh(chapter)
    return chapter


async def list_chapters(session: AsyncSession, story_id: UUID) -> list[Chapter]:
    result = await session.execute(select(Chapter).where(Chapter.story_id == story_id))
    return list(result.scalars())


async def search_chapters(session: AsyncSession, story_id: UUID, query_vec: list[float], k: int = 3) -> list[Chapter]:
    result = await session.execute(
        select(Chapter).where(Chapter.story_id == story_id).order_by(Chapter.embedding.l2_distance(query_vec)).limit(k)
    )
    return list(result.scalars())
