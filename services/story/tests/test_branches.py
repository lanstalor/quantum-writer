import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.db import database as db
from app.models.branch import Branch
from app.main import app

@pytest.fixture
async def test_app(monkeypatch):
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)

    async def override_get_db():
        async with TestSessionLocal() as session:
            yield session

    import app.main as app_main
    monkeypatch.setattr(db, "engine", test_engine, raising=False)
    monkeypatch.setattr(db, "AsyncSessionLocal", TestSessionLocal, raising=False)
    monkeypatch.setattr(app_main, "engine", test_engine, raising=False)
    app_main.app.dependency_overrides[db.get_db] = override_get_db

    from app.core import security
    app_main.app.dependency_overrides[security.get_current_user] = lambda: "user1"

    async with test_engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)

    yield app_main.app, TestSessionLocal

    app_main.app.dependency_overrides.clear()
    await test_engine.dispose()

@pytest.mark.asyncio
async def test_branch_crud(test_app):
    app, SessionLocal = test_app
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/stories/",
            json={"title": "My Story", "genre": "fantasy"},
        )
        assert resp.status_code == 200
        story_id = resp.json()["id"]

        resp = await ac.post(
            "/api/v1/branches/",
            json={"story_id": story_id, "name": "side", "description": "desc"},
        )
        assert resp.status_code == 200
        branch_id = resp.json()["id"]

        resp = await ac.get(f"/api/v1/branches/story/{story_id}")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

        resp = await ac.put(
            f"/api/v1/branches/{branch_id}",
            json={"name": "updated"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "updated"

        resp = await ac.delete(f"/api/v1/branches/{branch_id}")
        assert resp.status_code == 200

    async with SessionLocal() as session:
        result = await session.execute(select(Branch).where(Branch.story_id == story_id))
        branches = result.scalars().all()
        assert len(branches) == 1
        assert branches[0].is_main
