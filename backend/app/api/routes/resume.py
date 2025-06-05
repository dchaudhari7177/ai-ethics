from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from pathlib import Path

from app.db.base import get_db
from app.models.resume import Resume, Analysis, BiasMetrics
from app.ml.model import ResumeAnalyzer
from app.ml.bias import BiasDetector
from app.core.config import settings
from app.core.logging import logger

router = APIRouter()
resume_analyzer = ResumeAnalyzer()
bias_detector = BiasDetector()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and analyze a resume."""
    try:
        # Read and save resume content
        content = await file.read()
        content_str = content.decode()
        
        # Create resume record
        resume = Resume(
            filename=file.filename,
            content=content_str
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        # Extract features
        features = resume_analyzer.extract_features(content_str)
        resume.extracted_features = features
        
        # Analyze resume
        decision, confidence, feature_importance = resume_analyzer.predict(content_str)
        
        # Create analysis record
        analysis = Analysis(
            resume_id=resume.id,
            score=confidence,
            decision=decision,
            confidence=confidence,
            feature_importance=feature_importance,
            explanation=f"Decision based on {len(feature_importance)} features"
        )
        db.add(analysis)
        
        # Detect bias
        bias_metrics = bias_detector.detect_bias(
            features=pd.DataFrame([features]),
            predictions=np.array([1 if decision == "shortlist" else 0]),
            protected_attributes=features.get('protected_attributes', {})
        )
        
        # Create bias metrics record
        metrics = BiasMetrics(
            resume_id=resume.id,
            demographic_parity=bias_metrics['demographic_parity'],
            equal_opportunity=bias_metrics['equal_opportunity'],
            disparate_impact=bias_metrics['disparate_impact'],
            protected_attributes=features.get('protected_attributes', {}),
            mitigation_applied=None
        )
        db.add(metrics)
        
        db.commit()
        
        return {
            "resume_id": resume.id,
            "decision": decision,
            "confidence": confidence,
            "bias_metrics": bias_metrics,
            "feature_importance": feature_importance
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error processing resume"
        )

@router.get("/analysis/{resume_id}")
async def get_analysis(
    resume_id: int,
    db: Session = Depends(get_db)
):
    """Get analysis results for a resume."""
    analysis = db.query(Analysis).filter(Analysis.resume_id == resume_id).first()
    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )
    
    bias_metrics = db.query(BiasMetrics).filter(
        BiasMetrics.resume_id == resume_id
    ).first()
    
    return {
        "analysis": {
            "decision": analysis.decision,
            "confidence": analysis.confidence,
            "feature_importance": analysis.feature_importance,
            "explanation": analysis.explanation
        },
        "bias_metrics": {
            "demographic_parity": bias_metrics.demographic_parity,
            "equal_opportunity": bias_metrics.equal_opportunity,
            "disparate_impact": bias_metrics.disparate_impact,
            "protected_attributes": bias_metrics.protected_attributes,
            "mitigation_applied": bias_metrics.mitigation_applied
        } if bias_metrics else None
    }

@router.get("/list")
async def list_resumes(
    db: Session = Depends(get_db)
):
    """List all processed resumes."""
    resumes = db.query(Resume).all()
    return [{
        "id": resume.id,
        "filename": resume.filename,
        "created_at": resume.created_at,
        "analysis_results": [{
            "decision": analysis.decision,
            "confidence": analysis.confidence
        } for analysis in resume.analysis_results]
    } for resume in resumes] 