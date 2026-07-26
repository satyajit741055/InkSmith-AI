import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
        Load and Validate environment variables from .env
    """

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # OpenAI LLM Configuration
    OPENAI_API_KEY: str 

    # GroqAPI LLM Configuration
    GROQ_API_KEY: str 

    # Tavily API Configuration
    TAVILY_API_KEY: str
    GOOGLE_API_KEY: str
    HF_API_TOKEN: str

    #Output Directory 
    IMAGES_DIR: str = "images"
    OUTPUT_DIR: str = "output"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # --- OBSERVABILITY ---
    LOGFIRE_TOKEN: str | None = None
    LOGFIRE_BASE_URL: str | None = None
    LANGSMITH_TRACING: str = "true"
    LANGSMITH_API_KEY: str | None = None
    LANGSMITH_PROJECT: str = "blog_Agent"
    LANGSMITH_ENDPOINT: str = "https://api.smith.langchain.com"

settings = Settings()


def apply_langchain_env():
    """Write LangSmith/LangChain settings to os.environ for automatic tracing.

    Tracing is only activated when both LANGSMITH_TRACING and LANGSMITH_API_KEY
    are set — enabling tracing without a key causes LangChain to emit 401 noise
    on every LangGraph step.
    """
    if settings.LANGSMITH_TRACING and settings.LANGSMITH_API_KEY:
        os.environ.setdefault("LANGCHAIN_TRACING_V2", settings.LANGSMITH_TRACING)
        os.environ.setdefault("LANGCHAIN_API_KEY", settings.LANGSMITH_API_KEY)
    if settings.LANGSMITH_PROJECT:
        os.environ.setdefault("LANGCHAIN_PROJECT", settings.LANGSMITH_PROJECT)
    if settings.LANGSMITH_ENDPOINT:
        os.environ.setdefault("LANGCHAIN_ENDPOINT", settings.LANGSMITH_ENDPOINT)

apply_langchain_env()