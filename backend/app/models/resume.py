from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..db.base import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(String, nullable=False)
    extracted_features = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analysis results
    analysis_results = relationship("Analysis", back_populates="resume")
    bias_metrics = relationship("BiasMetrics", back_populates="resume")

class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    score = Column(Float, nullable=False)
    decision = Column(String, nullable=False)  # "shortlist" or "reject"
    confidence = Column(Float, nullable=False)
    feature_importance = Column(JSON)
    explanation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="analysis_results")

class BiasMetrics(Base):
    __tablename__ = "bias_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    demographic_parity = Column(Float)
    equal_opportunity = Column(Float)
    disparate_impact = Column(Float)
    protected_attributes = Column(JSON)
    mitigation_applied = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    resume = relationship("Resume", back_populates="bias_metrics") 