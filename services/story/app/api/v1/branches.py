from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db

router = APIRouter()

@router.get("/")
async def list_branches():
    """List branches - to be implemented"""
    return {"message": "Branches endpoint - to be implemented"}