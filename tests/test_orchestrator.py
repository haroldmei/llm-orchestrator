"""Tests for orchestrator"""
import pytest
from pathlib import Path
from src.core.orchestrator import FeatureEngineeringOrchestrator


class TestOrchestrator:
    
    def test_orchestrator_initialization(self):
        config = {
            "anthropic_api_key": "test_key",
            "model": "claude-sonnet-4-20250514",
            "max_iterations": 5,
            "confidence_threshold": 0.9,
        }
        orchestrator = FeatureEngineeringOrchestrator.__new__(FeatureEngineeringOrchestrator)
        orchestrator.config = config
        orchestrator.max_iterations = config["max_iterations"]
        orchestrator.confidence_threshold = config["confidence_threshold"]
        
        assert orchestrator.max_iterations == 5
        assert orchestrator.confidence_threshold == 0.9

