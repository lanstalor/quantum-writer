import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.db import database as db
from app.models.context import StoryContext
from app import core

@pytest.fixture
async def test_app(monkeypatch):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

    stored_segments = []

    async def fake_store(story_id: str, text: str):
        stored_segments.append({"story_id": story_id, "text": text})

    async def fake_search(story_id: str, query: str, limit: int = 5):
        results = [s for s in stored_segments if s["story_id"] == story_id]
        return [{"text": r["text"], "score": 1.0} for r in results[:limit]]

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    monkeypatch.setattr(db, "engine", test_engine, raising=False)
    monkeypatch.setattr(db, "AsyncSessionLocal", TestSessionLocal, raising=False)
    import app.main as app_main
    monkeypatch.setattr(app_main, "engine", test_engine, raising=False)
    app_main.app.dependency_overrides[db.get_db] = override_get_db
    monkeypatch.setattr(core, "store_context_segment", fake_store)
    monkeypatch.setattr(core, "search_story_segments", fake_search)

    async with test_engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    yield app_main.app, TestSessionLocal, stored_segments

    app_main.app.dependency_overrides.clear()
    await test_engine.dispose()

@pytest.mark.asyncio
async def test_save_and_get_context(test_app):
    app, SessionLocal, stored = test_app
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
    assert len(stored) == 1


@pytest.mark.asyncio
async def test_search_context(test_app):
    app, _, _ = test_app
    story_id = "story2"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(f"/api/v1/context/{story_id}", json={"content": "Dragons appear"})
        await ac.post(f"/api/v1/context/{story_id}", json={"content": "Hero fights dragon"})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get(f"/api/v1/context/{story_id}/search", params={"query": "dragon"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) >= 1
    assert "dragon" in data["results"][0]["text"].lower()
