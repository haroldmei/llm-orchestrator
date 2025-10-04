"""Tests for agents"""
import pytest
from src.agents.fe_reviewer import FEReviewer


class TestAgents:
    
    def test_confidence_score_extraction(self):
        config = {"anthropic_api_key": "test_key"}
        reviewer = FEReviewer(config)
        
        response = "Some review text\nCONFIDENCE_SCORE: 85%\nMore text"
        score = reviewer._extract_confidence_score(response)
        assert score == 0.85
        
        response = "CONFIDENCE_SCORE: 92%"
        score = reviewer._extract_confidence_score(response)
        assert score == 0.92

