import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
import json
import logging

from ..core.config import settings
from ..core.logging import logger, bias_logger

# Try to import AIF360 components, but don't fail if not available
try:
    from aif360.datasets import BinaryLabelDataset
    from aif360.metrics import BinaryLabelDatasetMetric
    from aif360.algorithms.preprocessing import Reweighing
    from aif360.algorithms.inprocessing import PrejudiceRemover
    from aif360.algorithms.postprocessing import EqOddsPostprocessing
    AIF360_AVAILABLE = True
except ImportError:
    logger.warning("AIF360 not available. Bias detection features will be limited.")
    AIF360_AVAILABLE = False

class BiasDetector:
    def __init__(self):
        """Initialize bias detection metrics."""
        self.metrics = {}
        self.protected_attributes = settings.PROTECTED_ATTRIBUTES
        self.mitigation_techniques = {
            'reweighing': self._apply_reweighing,
            'prejudice_remover': self._apply_prejudice_remover,
            'equalized_odds': self._apply_equalized_odds
        }
        
        if not AIF360_AVAILABLE:
            logger.warning("AIF360 is not available. Some bias detection features will be disabled.")
    
    def create_dataset(
        self,
        features: pd.DataFrame,
        labels: np.ndarray,
        protected_attribute_names: List[str]
    ) -> Any:
        """Create an AIF360 dataset from features and labels."""
        if not AIF360_AVAILABLE:
            return None
            
        return BinaryLabelDataset(
            df=features,
            label_names=['decision'],
            protected_attribute_names=protected_attribute_names,
            favorable_label=1,
            unfavorable_label=0
        )
    
    def compute_metrics(
        self,
        dataset: Any,
        privileged_groups: List[Dict],
        unprivileged_groups: List[Dict]
    ) -> Dict[str, float]:
        """Compute fairness metrics for the dataset."""
        if not AIF360_AVAILABLE:
            return {
                'demographic_parity': 0.0,
                'equal_opportunity': 0.0,
                'disparate_impact': 1.0
            }
            
        metrics = BinaryLabelDatasetMetric(
            dataset,
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups
        )
        
        results = {
            'demographic_parity': metrics.statistical_parity_difference(),
            'equal_opportunity': metrics.equal_opportunity_difference(),
            'disparate_impact': metrics.disparate_impact()
        }
        
        # Log metrics
        bias_logger.info(f"Fairness Metrics: {json.dumps(results, indent=2)}")
        
        return results
    
    def detect_bias(
        self,
        features: pd.DataFrame,
        predictions: np.ndarray,
        protected_attributes: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Detect bias in predictions based on protected attributes.
        
        Args:
            features: DataFrame containing resume features
            predictions: Array of binary predictions (1 for shortlist, 0 for reject)
            protected_attributes: Dictionary of protected attributes (e.g., gender, age)
            
        Returns:
            Dictionary containing bias metrics
        """
        try:
            # Calculate basic statistics
            total_candidates = len(predictions)
            shortlisted = np.sum(predictions)
            rejection_rate = 1 - (shortlisted / total_candidates)
            
            # Calculate demographic statistics
            demographic_stats = self._calculate_demographic_stats(
                predictions, protected_attributes
            )
            
            # Calculate fairness metrics
            fairness_metrics = self._calculate_fairness_metrics(
                predictions, protected_attributes
            )
            
            # Combine all metrics
            self.metrics = {
                "overall": {
                    "total_candidates": int(total_candidates),
                    "shortlisted": int(shortlisted),
                    "rejection_rate": float(rejection_rate)
                },
                "demographics": demographic_stats,
                "fairness": fairness_metrics
            }
            
            return self.metrics
            
        except Exception as e:
            logger.error(f"Error in bias detection: {str(e)}")
            return {
                "error": str(e),
                "overall": {
                    "total_candidates": int(total_candidates),
                    "shortlisted": int(shortlisted),
                    "rejection_rate": float(rejection_rate)
                }
            }
    
    def _calculate_demographic_stats(
        self,
        predictions: np.ndarray,
        protected_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate statistics for different demographic groups."""
        stats = {}
        
        # Calculate gender statistics
        if "gender" in protected_attributes:
            gender = protected_attributes["gender"]
            gender_shortlisted = np.sum(predictions)
            gender_total = len(predictions)
            stats["gender"] = {
                "value": gender,
                "shortlisted": int(gender_shortlisted),
                "total": int(gender_total),
                "shortlist_rate": float(gender_shortlisted / gender_total)
            }
        
        # Calculate age statistics
        if "age" in protected_attributes:
            age = protected_attributes["age"]
            age_group = self._get_age_group(age)
            stats["age"] = {
                "value": age,
                "group": age_group
            }
        
        return stats
    
    def _calculate_fairness_metrics(
        self,
        predictions: np.ndarray,
        protected_attributes: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate fairness metrics."""
        metrics = {}
        
        # Calculate demographic parity
        if "gender" in protected_attributes:
            gender_shortlist_rate = np.mean(predictions)
            metrics["demographic_parity"] = float(gender_shortlist_rate)
        
        # Calculate equal opportunity
        if "gender" in protected_attributes:
            metrics["equal_opportunity"] = float(np.mean(predictions))
        
        return metrics
    
    def _get_age_group(self, age: int) -> str:
        """Convert age to age group."""
        if age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"
        else:
            return "55+"
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get the latest bias metrics."""
        return self.metrics
    
    def mitigate_bias(
        self,
        features: pd.DataFrame,
        labels: np.ndarray,
        protected_attributes: Dict[str, Any],
        technique: str = 'reweighing'
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """Apply bias mitigation technique."""
        if technique not in self.mitigation_techniques:
            raise ValueError(f"Unknown mitigation technique: {technique}")
        
        # Create dataset
        dataset = self.create_dataset(
            features,
            labels,
            list(protected_attributes.keys())
        )
        
        # Apply mitigation
        mitigated_features, mitigated_labels = self.mitigation_techniques[technique](
            dataset,
            protected_attributes
        )
        
        bias_logger.info(f"Applied bias mitigation technique: {technique}")
        
        return mitigated_features, mitigated_labels
    
    def _apply_reweighing(
        self,
        dataset: BinaryLabelDataset,
        protected_attributes: Dict[str, Any]
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """Apply reweighing preprocessing technique."""
        privileged_groups = [{attr: 1} for attr in protected_attributes]
        unprivileged_groups = [{attr: 0} for attr in protected_attributes]
        
        rw = Reweighing(
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups
        )
        transformed_dataset = rw.fit_transform(dataset)
        
        return transformed_dataset.features, transformed_dataset.labels
    
    def _apply_prejudice_remover(
        self,
        dataset: BinaryLabelDataset,
        protected_attributes: Dict[str, Any]
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """Apply prejudice remover inprocessing technique."""
        pr = PrejudiceRemover(eta=0.1)
        transformed_dataset = pr.fit_transform(dataset)
        
        return transformed_dataset.features, transformed_dataset.labels
    
    def _apply_equalized_odds(
        self,
        dataset: BinaryLabelDataset,
        protected_attributes: Dict[str, Any]
    ) -> Tuple[pd.DataFrame, np.ndarray]:
        """Apply equalized odds postprocessing technique."""
        privileged_groups = [{attr: 1} for attr in protected_attributes]
        unprivileged_groups = [{attr: 0} for attr in protected_attributes]
        
        eqo = EqOddsPostprocessing(
            unprivileged_groups=unprivileged_groups,
            privileged_groups=privileged_groups
        )
        transformed_dataset = eqo.fit_transform(dataset)
        
        return transformed_dataset.features, transformed_dataset.labels 