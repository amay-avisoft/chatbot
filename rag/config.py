
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    OPENAI_API_KEY: str
    ORGANIZATION_NAME: str
    ORGANIZATION_SUMMARY: str

    class Config:
        env_file = ".env" 

# Initialize settings
settings = Settings()