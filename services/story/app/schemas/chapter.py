from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from datetime import datetime

class ChapterBase(BaseModel):
    title: str
    content: str
    position: Optional[int] = None

class ChapterCreate(ChapterBase):
    story_id: str
    branch_id: Optional[str] = None
    
class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    position: Optional[int] = None
    chapter_metadata: Optional[Dict[str, Any]] = None

class ChapterResponse(ChapterBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    story_id: str
    branch_id: Optional[str] = None
    word_count: int
    chapter_metadata: Optional[Dict[str, Any]] = {}
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class ChapterListResponse(BaseModel):
    id: str
    title: str
    position: int
    word_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class GenerateChapterRequest(BaseModel):
    story_id: str
    title: str = Field(..., description="Title for the new chapter")
    prompt: str = Field(..., description="Prompt for AI generation")
    position: Optional[int] = Field(default=None, description="Position in story (auto-calculated if not provided)")
    system_prompt: Optional[str] = Field(default="", description="System prompt for AI")