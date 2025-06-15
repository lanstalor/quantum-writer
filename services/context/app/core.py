from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SERVICE_NAME: str = "context-service"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/quantum_writer"
    MAX_CONTEXT_TOKENS: int = 4096

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
