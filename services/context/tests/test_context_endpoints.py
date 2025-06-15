import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.db import database as db
from app.models.context import StoryContext

@pytest.fixture
async def test_app(monkeypatch):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    monkeypatch.setattr(db, "engine", test_engine, raising=False)
    monkeypatch.setattr(db, "AsyncSessionLocal", TestSessionLocal, raising=False)
    import app.main as app_main
    monkeypatch.setattr(app_main, "engine", test_engine, raising=False)
    app_main.app.dependency_overrides[db.get_db] = override_get_db

    async with test_engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    yield app_main.app, TestSessionLocal

    app_main.app.dependency_overrides.clear()
    await test_engine.dispose()

@pytest.mark.asyncio
async def test_save_and_get_context(test_app):
    app, SessionLocal = test_app
    story_id = "story1"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(f"/api/v1/context/{story_id}", json={"content": "First part"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["story_id"] == story_id

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get(f"/api/v1/context/{story_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert "First part" in data["content"]

    async with SessionLocal() as session:
        result = await session.execute(select(StoryContext).where(StoryContext.story_id == story_id))
        ctx = result.scalar_one_or_none()
        assert ctx is not None
