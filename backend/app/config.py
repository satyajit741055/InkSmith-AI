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


settings = Settings()

    