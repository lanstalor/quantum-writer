from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ContextCreate(BaseModel):
    content: str

class ContextResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    story_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
