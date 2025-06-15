from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class StoryContext(Base):
    __tablename__ = "story_contexts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
