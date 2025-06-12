import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.db import database as db
from app.models.branch import Branch
from app.models.chapter import Chapter
from app.main import app

@pytest.fixture
async def test_app(monkeypatch):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    # patch database session and engine
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
async def test_create_story(test_app):
    app, SessionLocal = test_app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/stories/",
            json={"title": "My Story", "genre": "fantasy", "description": "desc"},
            headers={"X-User-Id": "user1"}
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "My Story"
    assert data["user_id"] == "user1"

    async with SessionLocal() as session:
        result = await session.execute(select(Branch).where(Branch.story_id == data["id"]))
        branches = result.scalars().all()
        assert len(branches) == 1
        assert branches[0].is_main

@pytest.mark.asyncio
async def test_generate_chapter(test_app, monkeypatch):
    app, SessionLocal = test_app

    # create story first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/stories/",
            json={"title": "My Story", "genre": "fantasy"},
            headers={"X-User-Id": "user1"}
        )
        story_id = resp.json()["id"]

    class FakeResponse:
        def __init__(self, data):
            self._data = data
            self.status_code = 200
        def raise_for_status(self):
            pass
        def json(self):
            return self._data

    async def fake_post(self, url, json=None, timeout=None):
        return FakeResponse({"content": "AI generated content"})

    monkeypatch.setattr("httpx.AsyncClient.post", fake_post)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/chapters/generate",
            json={
                "story_id": story_id,
                "title": "Chapter 1",
                "prompt": "Start",
                "position": 1
            }
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Chapter 1"
    assert data["content"] == "AI generated content"

    async with SessionLocal() as session:
        result = await session.execute(select(Chapter).where(Chapter.story_id == story_id))
        chapters = result.scalars().all()
        assert len(chapters) == 1
        assert chapters[0].title == "Chapter 1"
