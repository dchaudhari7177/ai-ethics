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

from app.core.config import settings
from app.core.logging import logger, model_logger, bias_logger

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class ResumeAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )
        self.feature_names = None
        self.explainer = None
        
    def preprocess_text(self, text: str) -> str:
        """Preprocess resume text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = ' '.join(text.split())
        
        # Lemmatization using spaCy
        doc = nlp(text)
        text = ' '.join([token.lemma_ for token in doc if not token.is_stop])
        
        return text
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """Extract relevant features from resume text."""
        doc = nlp(text)
        
        features = {
            'education_count': len([ent for ent in doc.ents if ent.label_ == 'ORG' and any(edu in ent.text.lower() for edu in ['university', 'college', 'school'])]),
            'experience_years': self._extract_experience_years(text),
            'skills': self._extract_skills(doc),
            'has_email': any(token.like_email for token in doc),
            'has_phone': any(token.like_num and len(token.text) >= 10 for token in doc)
        }
        
        return features
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract years of experience from text."""
        # Implement regex or rule-based extraction
        return 0  # Placeholder
    
    def _extract_skills(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract skills from document."""
        # Implement skill extraction logic
        return []  # Placeholder
    
    def train(self, X: List[str], y: List[int]):
        """Train the model on resume data."""
        # Preprocess text
        X_processed = [self.preprocess_text(text) for text in X]
        
        # Transform text to features
        X_vectorized = self.vectorizer.fit_transform(X_processed)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Train model
        self.model.fit(X_vectorized, y)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)
        
        # Save model and vectorizer
        self._save_model()
        
        logger.info("Model training completed")
    
    def predict(self, text: str) -> Tuple[str, float, Dict[str, float]]:
        """Predict whether to shortlist or reject a resume."""
        # Preprocess and vectorize
        processed_text = self.preprocess_text(text)
        features = self.vectorizer.transform([processed_text])
        
        # Make prediction
        prediction = self.model.predict(features)[0]
        confidence = np.max(self.model.predict_proba(features)[0])
        
        # Generate explanation
        if self.explainer:
            shap_values = self.explainer.shap_values(features)
            feature_importance = dict(zip(
                self.feature_names,
                shap_values[0] if isinstance(shap_values, list) else shap_values
            ))
        else:
            feature_importance = {}
        
        decision = "shortlist" if prediction == 1 else "reject"
        
        # Log the decision
        model_logger.info(
            f"Resume Analysis - Decision: {decision}, Confidence: {confidence:.2f}"
        )
        
        return decision, confidence, feature_importance
    
    def _save_model(self):
        """Save model and vectorizer to disk."""
        model_dir = Path(settings.MODEL_PATH)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, model_dir / "resume_model.joblib")
        joblib.dump(self.vectorizer, model_dir / "vectorizer.joblib")
        
        if self.feature_names is not None:
            with open(model_dir / "feature_names.json", 'w') as f:
                json.dump(list(self.feature_names), f)
    
    def load_model(self):
        """Load model and vectorizer from disk."""
        model_dir = Path(settings.MODEL_PATH)
        
        if not (model_dir / "resume_model.joblib").exists():
            raise FileNotFoundError("Model file not found")
        
        self.model = joblib.load(model_dir / "resume_model.joblib")
        self.vectorizer = joblib.load(model_dir / "vectorizer.joblib")
        
        with open(model_dir / "feature_names.json", 'r') as f:
            self.feature_names = json.load(f)
        
        self.explainer = shap.TreeExplainer(self.model)
        
        logger.info("Model loaded successfully") 