from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid

class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    story_id = Column(String, ForeignKey("stories.id"), nullable=False)
    parent_branch_id = Column(String, ForeignKey("branches.id"), nullable=True)
    
    name = Column(String(255), nullable=False)
    description = Column(Text)
    is_main = Column(Boolean, default=False)
    status = Column(String(50), default="active")  # active, merged, abandoned
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    story = relationship("Story", back_populates="branches")
    chapters = relationship("Chapter", back_populates="branch")
    child_branches = relationship("Branch", backref="parent_branch", remote_side=[id])