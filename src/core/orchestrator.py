"""Main orchestrator for managing agent workflow"""
import logging
from pathlib import Path
from typing import Dict, Any
from src.agents.base_agent import BaseAgent
from src.agents.fe_designer import FEDesigner
from src.agents.fe_reviewer import FEReviewer
from src.agents.fe_fixer import FEFixer
from src.utils.file_manager import FileManager
from src.utils.config_loader import ConfigLoader


class FeatureEngineeringOrchestrator:
    
    def __init__(self, config_path: str = "config/config.yaml", reviewer_type: str = "default"):
        self.config = ConfigLoader.load(config_path)
        self.file_manager = FileManager(self.config)
        self.logger = self._setup_logger()
        
        self.designer = FEDesigner(self.config)
        self.reviewer = self._create_reviewer(reviewer_type)
        self.fixer = FEFixer(self.config)
        
        self.max_iterations = self.config.get("max_iterations", 5)
        self.confidence_threshold = self.config.get("confidence_threshold", 0.9)
    
    def _create_reviewer(self, reviewer_type: str):
        """Factory method to create appropriate reviewer based on type"""
        if reviewer_type == "robust":
            from src.agents.fe_reviewer_robust import FEReviewerRobust
            self.logger.info("Using robust regex reviewer")
            return FEReviewerRobust(self.config)
        elif reviewer_type == "structured":
            from src.agents.fe_reviewer_improved import FEReviewerImproved
            self.logger.info("Using structured JSON reviewer")
            return FEReviewerImproved(self.config)
        else:
            self.logger.info("Using default regex reviewer")
            return FEReviewer(self.config)
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger("Orchestrator")
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler("logs/orchestrator.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def run(self, data_spec_path: str) -> Dict[str, Any]:
        self.logger.info("Starting Feature Engineering pipeline")
        
        fe_spec = self.designer.execute(data_spec_path)
        self.logger.info("Feature specification designed")
        
        iteration = 0
        while iteration < self.max_iterations:
            self.logger.info(f"Review iteration {iteration + 1}")
            
            review_result = self.reviewer.execute(
                fe_spec_path="specs/fe_spec.md",
                data_spec_path=data_spec_path
            )
            
            confidence_score = review_result["confidence_score"]
            self.logger.info(f"Confidence score: {confidence_score}")
            
            if confidence_score >= self.confidence_threshold:
                self.logger.info("Confidence threshold met. Pipeline complete.")
                return {
                    "status": "success",
                    "iterations": iteration + 1,
                    "confidence_score": confidence_score,
                    "final_spec": "specs/fe_spec_final.md"
                }
            
            self.logger.info("Fixing feature specification")
            fe_spec = self.fixer.execute(
                fe_spec_path="specs/fe_spec.md",
                review_path="specs/fe_spec_review.md",
                data_spec_path=data_spec_path
            )
            
            iteration += 1
        
        self.logger.warning(f"Max iterations ({self.max_iterations}) reached without meeting threshold")
        return {
            "status": "incomplete",
            "iterations": iteration,
            "confidence_score": confidence_score,
            "final_spec": "specs/fe_spec.md"
        }

