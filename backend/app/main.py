from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from .ml.model import ResumeAnalyzer
from .ml.bias import BiasDetector
from .db.init_db import save_resume, save_analysis
import pandas as pd
import numpy as np

app = FastAPI(title="Resume Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML models
resume_analyzer = ResumeAnalyzer()
bias_detector = BiasDetector()

@app.post("/api/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    gender: str = None,
    age: int = None
):
    """Analyze a resume file and return the results."""
    try:
        # Read resume content
        content = await file.read()
        content = content.decode('utf-8')
        
        # Save resume file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        save_resume(filename, content)
        
        # Extract features
        features = resume_analyzer.extract_features(content)
        features["protected_attributes"] = {
            "gender": gender,
            "age": age
        }
        
        # Predict
        decision, confidence, feature_importance = resume_analyzer.predict(content)
        
        # Bias detection
        bias_metrics = bias_detector.detect_bias(
            features=pd.DataFrame([features]),
            predictions=np.array([1 if decision == "shortlist" else 0]),
            protected_attributes={"gender": gender, "age": age}
        )
        
        # Prepare analysis result
        analysis_result = {
            "filename": filename,
            "features": features,
            "decision": decision,
            "confidence": confidence,
            "feature_importance": feature_importance,
            "bias_metrics": bias_metrics,
            "protected_attributes": {"gender": gender, "age": age},
            "analyzed_at": datetime.utcnow().isoformat()
        }
        
        # Save analysis
        analysis_filename = filename.replace('.txt', '_analysis.json')
        save_analysis(analysis_filename, analysis_result)
        
        return analysis_result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/{filename}")
async def get_analysis(filename: str):
    """Get analysis results for a specific resume."""
    try:
        analysis_path = os.path.join(
            os.path.dirname(__file__),
            '../../analysis',
            filename.replace('.txt', '_analysis.json')
        )
        
        if not os.path.exists(analysis_path):
            raise HTTPException(status_code=404, detail="Analysis not found")
            
        with open(analysis_path, 'r') as f:
            return json.load(f)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resumes")
async def list_resumes():
    """List all analyzed resumes."""
    try:
        analysis_dir = os.path.join(os.path.dirname(__file__), '../../analysis')
        resumes = []
        
        for filename in os.listdir(analysis_dir):
            if filename.endswith('_analysis.json'):
                with open(os.path.join(analysis_dir, filename), 'r') as f:
                    analysis = json.load(f)
                    resumes.append({
                        "filename": analysis["filename"],
                        "decision": analysis["decision"],
                        "confidence": analysis["confidence"],
                        "analyzed_at": analysis["analyzed_at"]
                    })
        
        return resumes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 