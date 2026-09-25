"""
Case Memory & Storage - Persistent case management
Stores investigation outcomes for learning and analytics
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Storage directory
STORAGE_DIR = Path(__file__).parent / "cases"
STORAGE_DIR.mkdir(exist_ok=True)


class CaseMemory:
    """Manages persistent case storage and retrieval."""
    
    def __init__(self, storage_dir: str = str(STORAGE_DIR)):
        """Initialize case memory."""
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True, parents=True)
        self.cases_file = self.storage_dir / "cases.json"
        self.outcomes_file = self.storage_dir / "outcomes.json"
        self.patterns_file = self.storage_dir / "patterns.json"
        
        # Load existing data
        self.cases: Dict[str, Dict[str, Any]] = self._load_json(self.cases_file)
        self.outcomes: List[Dict[str, Any]] = self._load_json(self.outcomes_file, default=[])
        self.patterns: Dict[str, Any] = self._load_json(self.patterns_file, default={})
    
    def _load_json(self, filepath: Path, default=None):
        """Load JSON from file."""
        try:
            if filepath.exists():
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load {filepath}: {e}")
        return default if default is not None else {}
    
    def _save_json(self, filepath: Path, data: Any):
        """Save JSON to file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save {filepath}: {e}")
    
    def save_case(self, case_data: Dict[str, Any]) -> bool:
        """Save a case to persistent storage."""
        try:
            case_id = case_data.get("case_id")
            if not case_id:
                logger.error("Case data missing case_id")
                return False
            
            # Add timestamp if not present
            if "saved_at" not in case_data:
                case_data["saved_at"] = datetime.now().isoformat()
            
            self.cases[case_id] = case_data
            self._save_json(self.cases_file, self.cases)
            logger.info(f"✓ Saved case {case_id}")
            return True
        except Exception as e:
            logger.error(f"✗ Error saving case: {e}")
            return False
    
    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a case from storage."""
        return self.cases.get(case_id)
    
    def get_all_cases(self) -> Dict[str, Dict[str, Any]]:
        """Get all stored cases."""
        return self.cases.copy()
    
    def record_outcome(self, outcome: Dict[str, Any]) -> bool:
        """Record investigation outcome for learning."""
        try:
            # Ensure required fields
            required = ["case_id", "actual_fraud", "predicted_fraud", "confidence"]
            if not all(k in outcome for k in required):
                logger.warning(f"Outcome missing required fields: {outcome}")
                return False
            
            # Add metadata
            outcome["recorded_at"] = datetime.now().isoformat()
            
            # Record outcome
            self.outcomes.append(outcome)
            self._save_json(self.outcomes_file, self.outcomes)
            
            # Update accuracy metrics
            self._update_metrics(outcome)
            
            logger.info(f"✓ Recorded outcome for {outcome['case_id']}")
            return True
        except Exception as e:
            logger.error(f"✗ Error recording outcome: {e}")
            return False
    
    def _update_metrics(self, outcome: Dict[str, Any]):
        """Update accuracy metrics from outcome."""
        predicted = outcome.get("predicted_fraud", False)
        actual = outcome.get("actual_fraud", False)
        confidence = outcome.get("confidence", 0.0)
        
        # Initialize metrics if needed
        if "metrics" not in self.patterns:
            self.patterns["metrics"] = {
                "total": 0,
                "correct": 0,
                "false_positives": 0,
                "false_negatives": 0,
                "avg_confidence": 0.0
            }
        
        metrics = self.patterns["metrics"]
        
        # Update counters
        metrics["total"] += 1
        if predicted == actual:
            metrics["correct"] += 1
        elif predicted and not actual:
            metrics["false_positives"] += 1
        elif not predicted and actual:
            metrics["false_negatives"] += 1
        
        # Update average confidence
        metrics["avg_confidence"] = (
            (metrics["avg_confidence"] * (metrics["total"] - 1) + confidence) 
            / metrics["total"]
        )
        
        self._save_json(self.patterns_file, self.patterns)
    
    def learn_patterns(self, threshold: float = 0.7) -> Dict[str, Any]:
        """Learn fraud patterns from historical outcomes."""
        patterns_learned = {}
        
        if len(self.outcomes) < 5:
            logger.info(f"Not enough outcomes ({len(self.outcomes)}) for pattern learning")
            return patterns_learned
        
        try:
            # Analyze high-confidence fraud cases
            high_confidence_fraud = [
                o for o in self.outcomes 
                if o.get("predicted_fraud") and o.get("confidence", 0) > threshold
            ]
            
            # Analyze false positives (predicted fraud but not actual)
            false_positives = [
                o for o in self.outcomes 
                if o.get("predicted_fraud") and not o.get("actual_fraud")
            ]
            
            patterns_learned = {
                "total_cases_analyzed": len(self.outcomes),
                "high_confidence_fraud_cases": len(high_confidence_fraud),
                "false_positive_rate": len(false_positives) / max(1, len(self.outcomes)),
                "confidence_threshold": threshold,
                "recommendations": self._generate_recommendations(patterns_learned)
            }
            
            logger.info(f"✓ Learned patterns from {len(self.outcomes)} outcomes")
            return patterns_learned
        except Exception as e:
            logger.error(f"✗ Error learning patterns: {e}")
            return patterns_learned
    
    def _generate_recommendations(self, patterns: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on patterns."""
        recommendations = []
        
        if patterns.get("false_positive_rate", 0) > 0.3:
            recommendations.append("High false positive rate detected. Consider adjusting detection thresholds.")
        
        if patterns.get("total_cases_analyzed", 0) > 100:
            recommendations.append("Sufficient historical data available. Consider retraining detection models.")
        
        if not recommendations:
            recommendations.append("System performing within normal parameters.")
        
        return recommendations
    
    def get_accuracy_metrics(self) -> Dict[str, Any]:
        """Get overall accuracy metrics."""
        if "metrics" not in self.patterns or not self.patterns["metrics"].get("total"):
            return {
                "accuracy": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "total_cases": 0
            }
        
        metrics = self.patterns["metrics"]
        total = metrics.get("total", 0)
        correct = metrics.get("correct", 0)
        fp = metrics.get("false_positives", 0)
        fn = metrics.get("false_negatives", 0)
        
        accuracy = correct / total if total > 0 else 0.0
        precision = correct / (correct + fp) if (correct + fp) > 0 else 0.0
        recall = correct / (correct + fn) if (correct + fn) > 0 else 0.0
        
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "total_cases": total,
            "correct_predictions": correct,
            "false_positives": fp,
            "false_negatives": fn
        }
    
    def export_cases(self, filepath: str) -> bool:
        """Export all cases to file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.cases, f, indent=2, default=str)
            logger.info(f"✓ Exported {len(self.cases)} cases to {filepath}")
            return True
        except Exception as e:
            logger.error(f"✗ Error exporting cases: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        return {
            "total_cases_stored": len(self.cases),
            "total_outcomes_recorded": len(self.outcomes),
            "accuracy_metrics": self.get_accuracy_metrics(),
            "storage_files": {
                "cases": str(self.cases_file),
                "outcomes": str(self.outcomes_file),
                "patterns": str(self.patterns_file)
            }
        }


# Global instance
_memory: Optional[CaseMemory] = None


def get_case_memory() -> CaseMemory:
    """Get or create global case memory instance."""
    global _memory
    if _memory is None:
        _memory = CaseMemory()
    return _memory
