from pydantic import BaseSettings
from typing import Dict, Any, List
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Resume Analysis API"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: str = os.getenv("PORT", "8000")
    NEXT_PUBLIC_API_URL: str = os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
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
    
    # File storage settings
    MODEL_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    RESUMES_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resumes")
    ANALYSIS_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "analysis")
    
    # Protected attributes for bias detection
    PROTECTED_ATTRIBUTES: Dict[str, Any] = {
        "gender": {
            "type": "categorical",
            "values": ["male", "female", "other"]
        },
        "age": {
            "type": "numerical",
            "min": 18,
            "max": 65
        }
    }
    
    # Bias detection thresholds
    BIAS_THRESHOLDS: Dict[str, float] = {
        "demographic_parity": 0.8,
        "equal_opportunity": 0.8,
        "disparate_impact": 0.8
    }

# Create global settings object
settings = Settings()

# Ensure required directories exist
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.RESUMES_DIR, exist_ok=True)
os.makedirs(settings.ANALYSIS_DIR, exist_ok=True) 