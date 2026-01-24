import json
from pathlib import Path
import joblib
import numpy as np
import warnings

# Suppress sklearn warnings about model compatibility
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*sklearn.*')


class ModelLoader:
    """Class to load and manage ML models"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.happiness_pipeline = None
        self.stress_pipeline = None
        self.persona_pipeline = None
        self.features = None
        self.persona_labels = None
        
    def load_models(self):
        """Load all ML models and metadata"""
        try:
            # Load pipelines
            self.happiness_pipeline = joblib.load(self.models_dir / "happiness_pipeline.joblib")
            self.stress_pipeline = joblib.load(self.models_dir / "stress_pipeline.joblib")
            self.persona_pipeline = joblib.load(self.models_dir / "persona_pipeline.joblib")
            
            # Load features list
            with open(self.models_dir / "features.json", "r") as f:
                self.features = json.load(f)
            
            # Load persona labels
            with open(self.models_dir / "persona_labels.json", "r") as f:
                self.persona_labels = json.load(f)
            
            print("✓ All models loaded successfully")
            return True
        except Exception as e:
            print(f"✗ Error loading models: {str(e)}")
            raise e
    
    def get_models(self):
        """Return all loaded models"""
        return {
            "happiness": self.happiness_pipeline,
            "stress": self.stress_pipeline,
            "persona": self.persona_pipeline,
            "features": self.features,
            "persona_labels": self.persona_labels
        }
