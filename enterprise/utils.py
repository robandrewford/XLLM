"""
Utility functions for enterprise features.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

class EnterpriseUtils:
    """Utility functions for enterprise features."""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading config from {config_path}: {e}")
            raise
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str) -> None:
        """Save configuration to JSON file."""
        try:
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving config to {config_path}: {e}")
            raise
    
    @staticmethod
    def validate_model_config(config: Dict[str, Any]) -> bool:
        """Validate model configuration."""
        required_fields = ["name", "version", "capabilities"]
        return all(field in config for field in required_fields)
    
    @staticmethod
    def get_model_path(model_name: str) -> Path:
        """Get path for model files."""
        return Path("models") / model_name 