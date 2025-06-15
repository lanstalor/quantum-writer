import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/register", json={"username": "alice", "password": "secret"})
        assert resp.status_code == 200
        data = resp.json()
        token = data["access_token"]
        refresh = data["refresh_token"]
        assert token and refresh

        resp = await ac.post("/login", json={"username": "alice", "password": "secret"})
        assert resp.status_code == 200
        login_data = resp.json()
        assert login_data["access_token"] and login_data["refresh_token"]

        resp = await ac.post("/refresh", params={"refresh": login_data["refresh_token"]})
        assert resp.status_code == 200
        refreshed = resp.json()
        assert refreshed["access_token"] and refreshed["refresh_token"]
