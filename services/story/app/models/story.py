from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Story(Base):
    __tablename__ = "stories"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    genre = Column(String(100))
    description = Column(Text)
    story_metadata = Column(JSON, default={})
    
    # User relationship
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    chapters = relationship("Chapter", back_populates="story", cascade="all, delete-orphan")
    branches = relationship("Branch", back_populates="story", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="story", cascade="all, delete-orphan")