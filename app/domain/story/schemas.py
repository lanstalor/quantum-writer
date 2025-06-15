from pydantic import BaseModel
from uuid import UUID
from datetime import datetime



class CreateStory(BaseModel):
    title: str


class StoryOut(BaseModel):
    id: UUID
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateChapter(BaseModel):
    story_id: UUID
    title: str
    content: str


class ChapterOut(BaseModel):
    id: UUID
    story_id: UUID
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
