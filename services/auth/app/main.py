from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict
from uuid import uuid4

from app.core import settings
from app.cloudflare import verify_access_token
from app.schemas import UserCreate, Token
from app.db.database import Base, engine, get_db
from app.models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Quantum Writer Auth Service", version="2.0.0", docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: Dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(authorization: str | None = None, db: AsyncSession = Depends(get_db)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.split(" ", 1)[1]
    username = decode_token(token)
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.SERVICE_NAME}


@app.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    refresh = create_refresh_token({"sub": user.username})
    db_user = User(
        username=user.username,
        hashed_password=get_password_hash(user.password),
        refresh_token=refresh,
    )
    db.add(db_user)
    await db.commit()
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "refresh_token": refresh, "token_type": "bearer"}


@app.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh: str, db: AsyncSession = Depends(get_db)):
    username = decode_token(refresh)
    result = await db.execute(select(User).where(User.username == username, User.refresh_token == refresh))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_refresh = create_refresh_token({"sub": username})
    user.refresh_token = new_refresh
    await db.commit()
    access = create_access_token({"sub": username})
    return {"access_token": access, "refresh_token": new_refresh, "token_type": "bearer"}


@app.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    refresh = create_refresh_token({"sub": user.username})
    db_user.refresh_token = refresh
    await db.commit()
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "refresh_token": refresh, "token_type": "bearer"}


@app.post("/login/cloudflare", response_model=Token)
async def login_with_cloudflare_access(
    request: Request,
    db: AsyncSession = Depends(get_db),
    cf_authorization: str | None = Header(default=None, alias="CF-Authorization"),
):
    token = cf_authorization or request.cookies.get("CF_Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Missing Cloudflare Access token")
    claims = await verify_access_token(token)

    email_claim = settings.CLOUDFLARE_ACCESS_EMAIL_CLAIM or "email"
    email = claims.get(email_claim) or claims.get("email") or claims.get("identity")
    if not email:
        raise HTTPException(status_code=400, detail="Cloudflare Access token missing email claim")
    username = email.lower()

    if settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS and username not in settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS:
        raise HTTPException(status_code=403, detail="Email not authorized")

    if settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAINS:
        domain = username.split("@")[-1]
        if domain not in settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAINS:
            raise HTTPException(status_code=403, detail="Email domain not authorized")

    result = await db.execute(select(User).where(User.username == username))
    db_user = result.scalar_one_or_none()
    if not db_user:
        random_password = uuid4().hex
        db_user = User(
            username=username,
            hashed_password=get_password_hash(random_password),
            refresh_token="",
        )
        db.add(db_user)
        await db.flush()

    refresh = create_refresh_token({"sub": username})
    db_user.refresh_token = refresh
    await db.commit()
    access = create_access_token({"sub": username})
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

