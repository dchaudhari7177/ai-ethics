from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.inprocessing import PrejudiceRemover
from aif360.algorithms.postprocessing import EqOddsPostprocessing
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from pathlib import Path
import json

from app.core.config import settings
from app.core.logging import logger, bias_logger

class BiasDetector:
    def __init__(self):
        self.protected_attributes = settings.PROTECTED_ATTRIBUTES
        self.metrics = {}
        self.mitigation_techniques = {
            'reweighing': self._apply_reweighing,
            'prejudice_remover': self._apply_prejudice_remover,
            'equalized_odds': self._apply_equalized_odds
        }
    
    def create_dataset(
        self,
        features: pd.DataFrame,
        labels: np.ndarray,
        protected_attribute_names: List[str]
    ) -> BinaryLabelDataset:
        """Create an AIF360 dataset from features and labels."""
        return BinaryLabelDataset(
            df=features,
            label_names=['decision'],
            protected_attribute_names=protected_attribute_names,
            favorable_label=1,
            unfavorable_label=0
        )
    
    def compute_metrics(
        self,
        dataset: BinaryLabelDataset,
        privileged_groups: List[Dict],
        unprivileged_groups: List[Dict]
    ) -> Dict[str, float]:
        """Compute fairness metrics for the dataset."""
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
        """Detect bias in model predictions."""
        # Create dataset
        dataset = self.create_dataset(
            features,
            predictions,
            list(protected_attributes.keys())
        )
        
        # Define privileged and unprivileged groups
        privileged_groups = [{attr: 1} for attr in protected_attributes]
        unprivileged_groups = [{attr: 0} for attr in protected_attributes]
        
        # Compute metrics
        metrics = self.compute_metrics(
            dataset,
            privileged_groups,
            unprivileged_groups
        )
        
        # Check against thresholds
        bias_detected = (
            abs(metrics['demographic_parity']) > (1 - settings.DEMOGRAPHIC_PARITY_THRESHOLD) or
            abs(metrics['equal_opportunity']) > (1 - settings.EQUAL_OPPORTUNITY_THRESHOLD) or
            abs(metrics['disparate_impact'] - 1) > (1 - settings.DISPARATE_IMPACT_THRESHOLD)
        )
        
        if bias_detected:
            bias_logger.warning("Bias detected in model predictions")
        
        return metrics
    
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