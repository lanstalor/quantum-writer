from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Chapter(Base):
    __tablename__ = "chapters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String, ForeignKey("stories.id"), nullable=False)
    branch_id = Column(String, ForeignKey("branches.id"), nullable=True)
    
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    position = Column(Integer, nullable=False)
    word_count = Column(Integer, default=0)
    chapter_metadata = Column(JSON, default={})
    
    # Version tracking
    version = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    story = relationship("Story", back_populates="chapters")
    branch = relationship("Branch", back_populates="chapters")