import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.config import get_settings
from .models import User
from .utils import hash_password, verify_password

settings = get_settings()


def create_access_token(user_id: uuid.UUID) -> str:
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


async def register(session: AsyncSession, email: str, password: str) -> User:
    user = User(email=email, password_hash=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate(session: AsyncSession, email: str, password: str) -> Optional[User]:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.password_hash):
        return user
    return None
