from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func
from typing import List
import uuid

from app.db.database import get_db
from app.models.branch import Branch
from app.models.chapter import Chapter
from app.models.story import Story
from app.schemas.branch import BranchCreate, BranchUpdate, BranchResponse
from app.core.security import get_current_user

router = APIRouter()

@router.post("/", response_model=BranchResponse)
async def create_branch(
    branch: BranchCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    result = await db.execute(
        select(Story).where(Story.id == branch.story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    db_branch = Branch(
        id=str(uuid.uuid4()),
        story_id=branch.story_id,
        parent_branch_id=branch.parent_branch_id,
        name=branch.name,
        description=branch.description,
        status=branch.status or "active",
        branch_metadata=branch.branch_metadata or {},
    )
    db.add(db_branch)
    await db.commit()
    await db.refresh(db_branch)
    return db_branch

@router.get("/story/{story_id}", response_model=List[BranchResponse])
async def list_branches(
    story_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    result = await db.execute(
        select(Story).where(Story.id == story_id, Story.user_id == user_id)
    )
    story = result.scalar_one_or_none()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    result = await db.execute(select(Branch).where(Branch.story_id == story_id))
    branches = result.scalars().all()
    return list(branches)

@router.put("/{branch_id}", response_model=BranchResponse)
async def update_branch(
    branch_id: str,
    branch_update: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    result = await db.execute(
        select(Branch)
        .join(Story, Branch.story_id == Story.id)
        .where(Branch.id == branch_id, Story.user_id == user_id)
    )
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    for field, value in branch_update.model_dump(exclude_unset=True).items():
        setattr(branch, field, value)
    await db.commit()
    await db.refresh(branch)
    return branch

@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    result = await db.execute(
        select(Branch)
        .join(Story, Branch.story_id == Story.id)
        .where(Branch.id == branch_id, Story.user_id == user_id)
    )
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    await db.delete(branch)
    await db.commit()
    return {"message": "Branch deleted successfully"}

@router.post("/{branch_id}/merge", response_model=BranchResponse)
async def merge_branch(
    branch_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    result = await db.execute(
        select(Branch)
        .join(Story, Branch.story_id == Story.id)
        .where(Branch.id == branch_id, Story.user_id == user_id)
    )
    branch = result.scalar_one_or_none()
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    if not branch.parent_branch_id:
        raise HTTPException(status_code=400, detail="Branch has no parent to merge into")
    if branch.status == "merged":
        raise HTTPException(status_code=400, detail="Branch already merged")

    result = await db.execute(select(Branch).where(Branch.id == branch.parent_branch_id))
    parent = result.scalar_one_or_none()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent branch not found")

    await db.execute(
        update(Chapter)
        .where(Chapter.branch_id == branch.id)
        .values(branch_id=parent.id, version=Chapter.version + 1)
    )

    branch.status = "merged"
    branch.merged_into_id = parent.id
    branch.merged_at = func.now()
    await db.commit()
    await db.refresh(branch)
    return branch
