from pydantic_settings import BaseSettings,SettingsConfigDict



class Settings(BaseSettings):
    """
        Load and Validate environment variables from .env
    """

    