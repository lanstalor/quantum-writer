from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


def _split_csv(value: str | list[str] | None) -> list[str]:
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    SERVICE_NAME: str = "auth-service"
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/quantum_writer"
    CLOUDFLARE_ACCESS_AUDIENCE: str | None = None
    CLOUDFLARE_ACCESS_TEAM_DOMAIN: str | None = None
    CLOUDFLARE_ACCESS_EMAIL_CLAIM: str = "email"
    CLOUDFLARE_ACCESS_ALLOWED_EMAILS: list[str] = Field(default_factory=list)
    CLOUDFLARE_ACCESS_ALLOWED_DOMAINS: list[str] = Field(default_factory=list)

    @field_validator(
        "CLOUDFLARE_ACCESS_ALLOWED_EMAILS", "CLOUDFLARE_ACCESS_ALLOWED_DOMAINS", mode="before"
    )
    @classmethod
    def _parse_csv(cls, value: str | list[str] | None) -> list[str]:
        return _split_csv(value)

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
