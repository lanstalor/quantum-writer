from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String, ForeignKey("stories.id"), nullable=False)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    role = Column(String(100))  # protagonist, antagonist, supporting, etc.
    traits = Column(JSON, default=[])
    relationships = Column(JSON, default={})
    arc = Column(Text)
    
    # For AI embeddings
    embedding_id = Column(String)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    story = relationship("Story", back_populates="characters")