import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.core import settings
from app.main import app
from app.models.user import User
from app.db import database


@pytest.fixture(autouse=True)
async def configure_settings():
    original_audience = settings.CLOUDFLARE_ACCESS_AUDIENCE
    original_domain = settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN
    original_allowed_emails = list(settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS)
    original_allowed_domains = list(settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAINS)
    original_claim = settings.CLOUDFLARE_ACCESS_EMAIL_CLAIM

    settings.CLOUDFLARE_ACCESS_AUDIENCE = "test-audience"
    settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN = "example.cloudflareaccess.com"
    settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS = []
    settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAINS = []
    settings.CLOUDFLARE_ACCESS_EMAIL_CLAIM = "email"
    yield
    settings.CLOUDFLARE_ACCESS_AUDIENCE = original_audience
    settings.CLOUDFLARE_ACCESS_TEAM_DOMAIN = original_domain
    settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS = original_allowed_emails
    settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAINS = original_allowed_domains
    settings.CLOUDFLARE_ACCESS_EMAIL_CLAIM = original_claim


@pytest.mark.asyncio
async def test_cloudflare_login_autoprovisions_user(monkeypatch):
    async def fake_verify(_: str):
        return {"email": "cf-user@example.com"}

    monkeypatch.setattr("app.main.verify_access_token", fake_verify)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/cloudflare", headers={"CF-Authorization": "token"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["access_token"]
        assert payload["refresh_token"]

    async with database.AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == "cf-user@example.com"))
        assert result.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_cloudflare_login_rejects_unknown_email(monkeypatch):
    async def fake_verify(_: str):
        return {"email": "blocked@example.com"}

    monkeypatch.setattr("app.main.verify_access_token", fake_verify)
    settings.CLOUDFLARE_ACCESS_ALLOWED_EMAILS = ["cf-user@example.com"]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/login/cloudflare", headers={"CF-Authorization": "token"})
        assert response.status_code == 403
