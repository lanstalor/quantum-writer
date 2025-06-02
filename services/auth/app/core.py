from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "auth-service"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
