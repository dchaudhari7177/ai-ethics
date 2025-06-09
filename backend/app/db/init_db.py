from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

from app.core.config import settings
from app.models.resume import Base, Resume, Analysis, BiasMetrics
from app.ml.model import ResumeAnalyzer
from app.ml.bias import BiasDetector

def init_db():
    """Initialize database with tables and sample data."""
    # Create database engine
    engine = create_engine("postgresql://admin:admin123@localhost:5432/mydb")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(Resume).count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create sample resumes
        sample_resumes = [
            {
                "filename": "john_doe_resume.pdf",
                "content": """
                John Doe
                Software Engineer
                
                Experience:
                - Senior Software Engineer at Tech Corp (2018-present)
                - Software Developer at StartupX (2015-2018)
                
                Education:
                - BS Computer Science, University of Technology
                
                Skills:
                Python, JavaScript, React, Machine Learning
                """,
                "protected_attributes": {
                    "gender": "male",
                    "age": 32
                }
            },
            {
                "filename": "jane_smith_resume.pdf",
                "content": """
                Jane Smith
                Data Scientist
                
                Experience:
                - Data Scientist at AI Solutions (2019-present)
                - Data Analyst at BigData Inc (2016-2019)
                
                Education:
                - MS Data Science, Tech University
                - BS Mathematics, State College
                
                Skills:
                Python, R, TensorFlow, Statistical Analysis
                """,
                "protected_attributes": {
                    "gender": "female",
                    "age": 28
                }
            },
            {
                "filename": "alex_johnson_resume.pdf",
                "content": """
                Alex Johnson
                Full Stack Developer
                
                Experience:
                - Full Stack Developer at WebTech (2017-present)
                - Frontend Developer at AppCo (2015-2017)
                
                Education:
                - BS Software Engineering, Tech Institute
                
                Skills:
                JavaScript, TypeScript, Node.js, React, MongoDB
                """,
                "protected_attributes": {
                    "gender": "non-binary",
                    "age": 30
                }
            }
        ]
        
        # Initialize ML models
        resume_analyzer = ResumeAnalyzer()
        bias_detector = BiasDetector()
        
        # Add sample data
        for resume_data in sample_resumes:
            # Create resume
            resume = Resume(
                filename=resume_data["filename"],
                content=resume_data["content"]
            )
            db.add(resume)
            db.flush()
            
            # Extract features
            features = resume_analyzer.extract_features(resume_data["content"])
            resume.extracted_features = {
                **features,
                "protected_attributes": resume_data["protected_attributes"]
            }
            
            # Analyze resume
            decision, confidence, feature_importance = resume_analyzer.predict(
                resume_data["content"]
            )
            
            # Create analysis
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
                protected_attributes=resume_data["protected_attributes"]
            )
            
            # Create bias metrics
            metrics = BiasMetrics(
                resume_id=resume.id,
                demographic_parity=bias_metrics["demographic_parity"],
                equal_opportunity=bias_metrics["equal_opportunity"],
                disparate_impact=bias_metrics["disparate_impact"],
                protected_attributes=resume_data["protected_attributes"],
                mitigation_applied=None
            )
            db.add(metrics)
        
        # Commit changes
        db.commit()
        print("Database initialized with sample data")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 