import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_character_extraction():
    text = "Alice and Bob met Charlie. Alice greeted Bob."
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/analyze/characters", json={"text": text})
    assert resp.status_code == 200
    data = resp.json()
    assert set(["Alice", "Bob", "Charlie"]).issubset(set(data["characters"]))

@pytest.mark.asyncio
async def test_plot_analysis():
    text = "Alice went to town. Bob followed. They found treasure."
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/api/v1/analyze/plot", json={"text": text})
    assert resp.status_code == 200
    data = resp.json()
    assert "summary" in data and data["summary"]
    assert data["sentence_count"] == 3
