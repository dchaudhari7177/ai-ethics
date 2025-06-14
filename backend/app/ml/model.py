import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import nltk
import spacy
from typing import Dict, List, Tuple, Any
import joblib
from pathlib import Path
import shap
import json
import re
import os

from ..core.config import settings
from ..core.logging import logger, model_logger, bias_logger

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("Downloading spaCy model...")
    spacy.cli.download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

class ResumeAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        
        # Initialize with sample data to fit the vectorizer
        self._initialize_with_sample_data()
    
    def _initialize_with_sample_data(self):
        """Initialize the model with sample resumes to fit the vectorizer."""
        sample_resumes = [
            """
            Software Engineer with 5 years of experience in Python and JavaScript.
            Strong background in web development and machine learning.
            Experience with React, Node.js, and TensorFlow.
            """,
            """
            Data Scientist with expertise in statistical analysis and machine learning.
            Proficient in Python, R, and SQL.
            Experience with pandas, scikit-learn, and deep learning frameworks.
            """,
            """
            Full Stack Developer with experience in modern web technologies.
            Skilled in JavaScript, TypeScript, and cloud platforms.
            Strong background in frontend and backend development.
            """
        ]
        
        # Fit the vectorizer with sample data
        self.vectorizer.fit(sample_resumes)
        
        # Create dummy labels for initial training
        dummy_labels = np.array([1, 1, 0])  # 1 for shortlist, 0 for reject
        X = self.vectorizer.transform(sample_resumes)
        self.classifier.fit(X, dummy_labels)
    
    def preprocess_text(self, text):
        """Clean and preprocess the resume text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Lemmatize using spaCy
        doc = nlp(text)
        lemmatized = ' '.join([token.lemma_ for token in doc])
        
        return lemmatized
    
    def extract_features(self, text):
        """Extract features from resume text."""
        processed_text = self.preprocess_text(text)
        
        # Get TF-IDF features
        features = self.vectorizer.transform([processed_text])
        
        # Extract named entities using spaCy
        doc = nlp(text)
        entities = {ent.label_: ent.text for ent in doc.ents}
        
        # Extract skills (simple keyword matching)
        skills = self._extract_skills(text)
        
        # Extract experience (simple pattern matching)
        experience = self._extract_experience(text)
        
        return {
            'tfidf_features': features.toarray()[0].tolist(),
            'entities': entities,
            'skills': skills,
            'experience': experience
        }
    
    def _extract_skills(self, text):
        """Extract skills from resume text."""
        # Common programming languages and technologies
        skills_list = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby',
            'php', 'swift', 'kotlin', 'go', 'rust', 'sql', 'nosql', 'mongodb',
            'postgresql', 'mysql', 'redis', 'react', 'angular', 'vue', 'node.js',
            'django', 'flask', 'spring', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'aws', 'azure', 'gcp', 'docker', 'kubernetes'
        ]
        
        found_skills = []
        for skill in skills_list:
            if skill.lower() in text.lower():
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_experience(self, text):
        """Extract experience information from resume text."""
        # Simple pattern matching for years of experience
        experience_pattern = r'(\d+)\s*(?:years?|yrs?)\s*(?:of)?\s*experience'
        match = re.search(experience_pattern, text.lower())
        
        if match:
            return int(match.group(1))
        return 0
    
    def predict(self, text):
        """Predict whether to shortlist the resume."""
        processed_text = self.preprocess_text(text)
        features = self.vectorizer.transform([processed_text])
        
        # Get prediction probability
        proba = self.classifier.predict_proba(features)[0]
        decision = "shortlist" if proba[1] > 0.5 else "reject"
        confidence = float(proba[1] if decision == "shortlist" else proba[0])
        
        # Get feature importance
        feature_names = self.vectorizer.get_feature_names_out()
        feature_importance = dict(zip(feature_names, self.classifier.feature_importances_))
        
        return decision, confidence, feature_importance
    
    def train(self, X: List[str], y: List[int]):
        """Train the model on resume data."""
        # Preprocess text
        X_processed = [self.preprocess_text(text) for text in X]
        
        # Transform text to features
        X_vectorized = self.vectorizer.fit_transform(X_processed)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Train model
        self.classifier.fit(X_vectorized, y)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.classifier)
        
        # Save model and vectorizer
        self._save_model()
        
        logger.info("Model training completed")
    
    def _save_model(self):
        """Save model and vectorizer to disk."""
        model_dir = Path(settings.MODEL_PATH)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.classifier, model_dir / "resume_model.joblib")
        joblib.dump(self.vectorizer, model_dir / "vectorizer.joblib")
        
        if self.feature_names is not None:
            with open(model_dir / "feature_names.json", 'w') as f:
                json.dump(list(self.feature_names), f)
    
    def load_model(self):
        """Load model and vectorizer from disk."""
        model_dir = Path(settings.MODEL_PATH)
        
        if not (model_dir / "resume_model.joblib").exists():
            raise FileNotFoundError("Model file not found")
        
        self.classifier = joblib.load(model_dir / "resume_model.joblib")
        self.vectorizer = joblib.load(model_dir / "vectorizer.joblib")
        
        with open(model_dir / "feature_names.json", 'r') as f:
            self.feature_names = json.load(f)
        
        self.explainer = shap.TreeExplainer(self.classifier)
        
        logger.info("Model loaded successfully") 