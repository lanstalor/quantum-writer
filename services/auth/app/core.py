from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "auth-service"
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
