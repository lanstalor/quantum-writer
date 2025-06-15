import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.session import get_db
from app.db.base import Base

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def session():
    engine = create_async_engine(DATABASE_URL)
    TestSession = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestSession() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def client(session):
    async def override_db():
        async with session.begin():
            yield session
    app.dependency_overrides[get_db] = override_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_story_flow(client: AsyncClient, session: AsyncSession):
    # register
    resp = await client.post("/auth/register", json={"email": "a@test.com", "password": "pass"})
    assert resp.status_code == 200
    # login
    resp = await client.post("/auth/login", json={"email": "a@test.com", "password": "pass"})
    # create story
    resp = await client.post("/stories/", json={"title": "My Story"})
    assert resp.status_code == 200
    story_id = resp.json()["id"]
    # create chapter
    resp = await client.post(f"/stories/{story_id}/chapters", json={"story_id": story_id, "title": "Ch1", "content": "hello"})
    assert resp.status_code == 200
    # search
    resp = await client.get(f"/stories/{story_id}/chapters/search", params={"q": "hello"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
