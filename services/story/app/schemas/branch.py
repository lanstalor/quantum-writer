from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class BranchBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_branch_id: Optional[str] = None
    branch_metadata: Optional[Dict[str, Any]] = {}
    status: Optional[str] = "active"

class BranchCreate(BranchBase):
    story_id: str

class BranchUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_branch_id: Optional[str] = None
    branch_metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class BranchResponse(BranchBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    story_id: str
    is_main: bool = False
    merged_into_id: Optional[str] = None
    merged_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
