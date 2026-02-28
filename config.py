import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NEO4J_URI: str
    NEO4J_USERNAME: str
    NEO4J_PASSWORD: str
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str | None = None
    LLM_MODEL: str
    EMBEDDING_MODEL: str
    EMBEDDING_DIMS: int
    PORT: int = 3899
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(env_file=".env")

# The settings instance
settings = Settings()
