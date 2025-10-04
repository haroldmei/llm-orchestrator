"""Configuration loader"""
import yaml
from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigLoader:
    
    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        path = Path(config_path)
        
        if not path.exists():
            return ConfigLoader._get_default_config()
        
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
        
        config = ConfigLoader._merge_env_vars(config)
        return config
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        return {
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "model": "claude-sonnet-4-20250514",
            "max_iterations": 5,
            "confidence_threshold": 0.9,
            "data_dir": "data",
            "specs_dir": "specs",
            "logs_dir": "logs",
        }
    
    @staticmethod
    def _merge_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
        if "anthropic_api_key" not in config or not config["anthropic_api_key"]:
            config["anthropic_api_key"] = os.getenv("ANTHROPIC_API_KEY", "")
        
        return config

