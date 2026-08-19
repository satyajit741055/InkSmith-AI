from pydantic import Field, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

class Settings(BaseSettings):
    """
    Load and validate environment variables for the application.    
    Fails fast at startup if any validation fails, preventing runtime errors.
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
    POSTGRES_ECHO: bool = False
    CHECKPOINTER_DB_URI: str

    # Redis Configurations
    REDIS_URL: str

    # JWT Configurations
    SECRET_KEY: str = Field(..., min_length=32)  # Minimum 32 characters for security
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM Configurations
    OPENAI_API_KEY: str = Field(..., min_length=20)  # OpenAI keys are ~48 chars
    GROQ_API_KEY: str = Field(..., min_length=20)    # Groq keys are ~32 chars
    HF_API_KEY: str = Field(..., min_length=20)      # HF keys are ~34 chars
    DEEPSEEK_API_KEY: str = Field(..., min_length=20)  # DeepSeek keys are ~48 chars

    # Output Directory 
    OUTPUT_DIR: str = "blogs"
    IMAGE_OUT_DIR: str = "blogs/images"  # Images stored inside blogs directory for shared volume

    # Tavily 
    TAVILY_API_KEY: str = Field(..., min_length=20)  # Tavily keys are ~32 chars

    # Storage Backend
    BACKEND: str = "local"
    # Environment
    ENVIRONMENT: str = "local"


    # S3 Configuration
    S3_BUCKET_NAME: str | None = None
    S3_REGION: str = "ap-south-1"
    S3_ACCESS_KEY_ID: SecretStr | None = None
    S3_SECRET_ACCESS_KEY: SecretStr | None = None
    S3_ENDPOINT_URL: str | None = None

    # CORS Configuration
    CORS_ORIGINS: str = Field(
    default="http://localhost:5173,http://localhost:3000,http://localhost:8001",
    description="Comma-separated list of allowed CORS origins"
)

    # API Configuration (for frontend)
    API_BASE_URL: str = Field(
        default="http://localhost:8001/api/v1",
        description="Backend API base URL (used by frontend)"
    )

    # LangSmith Tracing Configuration
    LANGSMITH_TRACING: str = Field(
        default="false",
        description="Enable LangSmith tracing (true/false). Only activates if LANGSMITH_API_KEY is set."
    )
    LANGSMITH_API_KEY: str | None = Field(
        default=None,
        description="LangSmith API key for tracing. Leave empty to disable tracing."
    )
    LANGSMITH_PROJECT: str = Field(
        default="ink-smith",
        description="LangSmith project name for organizing traces"
    )
    LANGSMITH_ENDPOINT: str = Field(
        default="https://api.smith.langchain.com",
        description="LangSmith API endpoint"
    )

    # Validators
    @field_validator('OPENAI_API_KEY', 'GROQ_API_KEY', 'HF_API_KEY', 'DEEPSEEK_API_KEY', 'TAVILY_API_KEY')
    @classmethod
    def validate_api_keys_not_placeholder(cls, v):
        """Ensure API keys are not empty or placeholder values."""
        if not v or v in ('sk-xxx', 'gsk-xxx', 'hf_xxx', 'tvly-xxx', 'placeholder'):
            raise ValueError(f"API key cannot be empty or placeholder value")
        if v.startswith('xxx') or v.endswith('xxx'):
            raise ValueError(f"API key looks like a placeholder (contains 'xxx')")
        return v

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure SECRET_KEY is strong enough for JWT."""
        if len(v) < 32:
            raise ValueError(f"SECRET_KEY must be at least 32 characters (got {len(v)})")
        # Check for common weak password patterns
        weak_patterns = ['password', '123456', 'secret', 'admin', 'test']
        if any(pattern in v.lower() for pattern in weak_patterns):
            raise ValueError(f"SECRET_KEY contains common weak password patterns")
        return v

    @field_validator('POSTGRES_URL', 'POSTGRES_URL_SYNC', 'CHECKPOINTER_DB_URI')
    @classmethod
    def validate_db_urls(cls, v):
        """Ensure database URLs are valid PostgreSQL URLs."""
        if not v.startswith(('postgresql://', 'postgresql+asyncpg://', 'postgresql+psycopg2://')):
            raise ValueError(f"Invalid database URL format (must start with postgresql://)")
        if '@' not in v:
            raise ValueError(f"Database URL must contain credentials (@)")
        return v

    @field_validator('REDIS_URL')
    @classmethod
    def validate_redis_url(cls, v):
        """Ensure Redis URL is valid."""
        if not v.startswith('redis://'):
            raise ValueError(f"Invalid Redis URL format (must start with redis://)")
        return v


settings = Settings()  # Raises ValidationError if any validation fails


def apply_langchain_env():
    """
    Configure LangSmith tracing for automatic instrumentation of LangGraph.
    
    Tracing is only activated when BOTH conditions are met:
    1. LANGSMITH_TRACING is "true" (case-insensitive)
    2. LANGSMITH_API_KEY is set and not empty

    """
    import logging
    logger = logging.getLogger(__name__)
    
    # Check if tracing is enabled
    tracing_enabled = settings.LANGSMITH_TRACING.lower() == "true"
    api_key_set = bool(settings.LANGSMITH_API_KEY and settings.LANGSMITH_API_KEY.strip())
    
    if tracing_enabled and api_key_set:
  
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGSMITH_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGSMITH_PROJECT
        os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGSMITH_ENDPOINT
        
        logger.info(f"✅ LangSmith tracing enabled (project: {settings.LANGSMITH_PROJECT})")
    
    elif tracing_enabled and not api_key_set:
        logger.warning(
            "⚠️ LangSmith tracing requested but LANGSMITH_API_KEY not set. "
            "Tracing disabled to avoid 401 errors on every LLM call. "
            "Set LANGSMITH_API_KEY to enable tracing."
        )
    
    else:
        logger.debug("ℹ️ LangSmith tracing disabled (LANGSMITH_TRACING=false)")


# Apply LangSmith configuration at startup
apply_langchain_env()