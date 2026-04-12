from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Explicitly load .env file BEFORE creating Settings
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

# Check if DATABASE_URL was loaded from .env
db_url_from_env = os.getenv("DATABASE_URL")
print(f"DEBUG: DATABASE_URL from os.getenv = {db_url_from_env}")


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/civil_defense_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB
    
    # JWT
    JWT_SECRET_KEY: str = "your-jwt-secret-key-change-in-production"
    
    # Application
    DEBUG: bool = False
    
    model_config = ConfigDict(extra="ignore")


settings = Settings()

# Debug: Print what DATABASE_URL is being used
print(f"DEBUG: .env path = {env_path}")
print(f"DEBUG: .env exists = {env_path.exists()}")
print(f"DEBUG: DATABASE_URL = {settings.DATABASE_URL}")
# Extract password for debugging
if "://" in settings.DATABASE_URL:
    parts = settings.DATABASE_URL.split("://")[1].split("@")[0]
    user_pass = parts.split(":")
    if len(user_pass) == 2:
        print(f"DEBUG: Database User = {user_pass[0]}")
        print(f"DEBUG: Database Password = {user_pass[1]}")
