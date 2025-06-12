import os
import pytest
from httpx import AsyncClient

@pytest.fixture
async def ai_app(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test")

    from app.main import app
    from app.services.groq_service import groq_service
    from app.services.openai_service import openai_service
    from app.services.anthropic_service import anthropic_service

    async def fake_generate_content(*args, **kwargs):
        return "Generated"

    def fake_estimate_tokens(text: str) -> int:
        return len(text) // 4

    for service in (groq_service, openai_service, anthropic_service):
        monkeypatch.setattr(service, "generate_content", fake_generate_content)
        monkeypatch.setattr(service, "estimate_tokens", fake_estimate_tokens)

    yield app

@pytest.mark.asyncio
async def test_generate_endpoint(ai_app):
    async with AsyncClient(app=ai_app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/generate",
            json={"prompt": "Hello", "context": "", "system_prompt": ""}
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["content"] == "Generated"
    assert data["tokens_used"] == len("Generated") // 4

@pytest.mark.asyncio
async def test_continue_story_endpoint(ai_app):
    async with AsyncClient(app=ai_app, base_url="http://test") as ac:
        resp = await ac.post(
            "/api/v1/continue-story",
            json={"prompt": "Next", "context": ""}
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["content"] == "Generated"
