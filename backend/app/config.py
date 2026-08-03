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
    POSTGRES_URL_SYNC: str
    POSTGRES_ECHO: bool = True

    # Redis Configurations
    REDIS_URL: str

    # JWT Configurations
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM Configurations
    OPENAI_API_KEY: str
    GROQ_API_KEY: str

    # Output Directory 
    OUTPUT_DIR: str = "blogs"


settings = Settings()