from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EthicalHire"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "Dipak@4646")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "ethicalhire")
    SQLALCHEMY_DATABASE_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]
    
    # ML Model Settings
    MODEL_PATH: Path = Path("app/ml/models")
    RESUME_UPLOAD_DIR: Path = Path("app/uploads/resumes")
    
    # Bias Detection
    PROTECTED_ATTRIBUTES: List[str] = [
        "gender",
        "race",
        "age",
        "nationality"
    ]
    
    # Fairness Thresholds
    DEMOGRAPHIC_PARITY_THRESHOLD: float = 0.8
    EQUAL_OPPORTUNITY_THRESHOLD: float = 0.8
    DISPARATE_IMPACT_THRESHOLD: float = 0.8
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# Create global settings object
settings = Settings()

# Ensure required directories exist
settings.MODEL_PATH.mkdir(parents=True, exist_ok=True)
settings.RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True) 