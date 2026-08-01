from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):

    """
    Load and validate environment variables for the application.
    """
    model_config = SettingsConfigDict(
    env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Database Configurations 
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_URL: str
    POSTGRES_ECHO: bool = True

    # Redis Configurations
    REDIS_URL: str


settings = Settings()