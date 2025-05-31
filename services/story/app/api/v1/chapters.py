from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db

router = APIRouter()

@router.get("/")
async def list_chapters():
    """List chapters - to be implemented"""
    return {"message": "Chapters endpoint - to be implemented"}