import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
from ..ml.model import ResumeAnalyzer
from ..ml.bias import BiasDetector

# Folders for resumes and analysis results
RESUME_DIR = os.path.join(os.path.dirname(__file__), '../../resumes')
ANALYSIS_DIR = os.path.join(os.path.dirname(__file__), '../../analysis')

os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DIR, exist_ok=True)

def save_resume(filename, content):
    """Save resume content to a file."""
    path = os.path.join(RESUME_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

def save_analysis(filename, data):
    """Save analysis results to a JSON file."""
    path = os.path.join(ANALYSIS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return path

def main():
    """Initialize the system with sample resumes and analyze them."""
    print("Initializing resume analysis system...")
    
    # Sample resumes for testing
    sample_resumes = [
        {
            "filename": "john_doe_resume.txt",
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
            "protected_attributes": {"gender": "male", "age": 32}
        },
        {
            "filename": "jane_smith_resume.txt",
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
            "protected_attributes": {"gender": "female", "age": 28}
        },
        {
            "filename": "alex_johnson_resume.txt",
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
            "protected_attributes": {"gender": "non-binary", "age": 30}
        }
    ]

    print("Initializing ML models...")
    resume_analyzer = ResumeAnalyzer()
    bias_detector = BiasDetector()

    print("Processing sample resumes...")
    for resume_data in sample_resumes:
        print(f"\nProcessing {resume_data['filename']}...")
        
        # Save resume file
        save_resume(resume_data["filename"], resume_data["content"])
        print(f"Saved resume to {RESUME_DIR}")

        # Extract features
        features = resume_analyzer.extract_features(resume_data["content"])
        features["protected_attributes"] = resume_data["protected_attributes"]
        print("Features extracted successfully")

        # Predict
        decision, confidence, feature_importance = resume_analyzer.predict(resume_data["content"])
        print(f"Prediction: {decision} (confidence: {confidence:.2f})")

        # Bias detection
        bias_metrics = bias_detector.detect_bias(
            features=pd.DataFrame([features]),
            predictions=np.array([1 if decision == "shortlist" else 0]),
            protected_attributes=resume_data["protected_attributes"]
        )
        print("Bias analysis completed")

        # Save analysis result
        analysis_result = {
            "filename": resume_data["filename"],
            "features": features,
            "decision": decision,
            "confidence": confidence,
            "feature_importance": feature_importance,
            "bias_metrics": bias_metrics,
            "protected_attributes": resume_data["protected_attributes"],
            "analyzed_at": datetime.utcnow().isoformat()
        }
        analysis_filename = resume_data["filename"].replace('.txt', '_analysis.json')
        save_analysis(analysis_filename, analysis_result)
        print(f"Analysis saved to {ANALYSIS_DIR}")

    print("\nInitialization completed successfully!")
    print(f"Resumes are stored in: {RESUME_DIR}")
    print(f"Analysis results are stored in: {ANALYSIS_DIR}")

if __name__ == "__main__":
    main()
