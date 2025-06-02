from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "websocket-service"
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
