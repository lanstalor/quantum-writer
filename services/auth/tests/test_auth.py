import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/register", json={"username": "alice", "password": "secret"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        assert token

        resp = await ac.post("/login", json={"username": "alice", "password": "secret"})
        assert resp.status_code == 200
        assert resp.json()["access_token"]
