from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Info
    PROJECT_NAME: str = "Map Recommendations API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()