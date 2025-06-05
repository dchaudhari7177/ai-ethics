from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Any
import uvicorn
import json
from pathlib import Path

# Import our modules
from app.core.config import settings
from app.api.routes import resume, analysis, metrics
from app.core.logging import setup_logging

# Create FastAPI app
app = FastAPI(
    title="EthicalHire API",
    description="AI Ethics in Recruitment - Backend API",
    version="1.0.0"
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/v1/resumes", tags=["resumes"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to EthicalHire API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Setup logging
    setup_logging()
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 