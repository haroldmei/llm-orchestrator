"""Feature Engineering Reviewer Agent"""
from pathlib import Path
from typing import Dict, Any
import re
from src.agents.base_agent import BaseAgent


class FEReviewer(BaseAgent):
    
    def get_prompt_template(self) -> str:
        prompt_path = Path("prompts/dl_fe_reviewer.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        return ""
    
    def execute(self, fe_spec_path: str, data_spec_path: str) -> Dict[str, Any]:
        self.logger.info(f"Reviewing feature specification: {fe_spec_path}")
        
        fe_spec = Path(fe_spec_path).read_text(encoding='utf-8')
        data_spec = Path(data_spec_path).read_text(encoding='utf-8')
        prompt_template = self.get_prompt_template()
        
        prompt = f"""{prompt_template}

# Original Data Specification
{data_spec}

# Feature Specification to Review
{fe_spec}

Please review the feature specification and provide:
1. A detailed review with suggestions for improvement
2. A confidence score (0-100%) indicating how confident you are that this specification can implement the data specification

Format the confidence score as: CONFIDENCE_SCORE: XX%"""
        
        response = self.call_claude(prompt)
        
        confidence_score = self._extract_confidence_score(response)
        
        review_path = Path("specs/fe_spec_review.md")
        review_path.write_text(response, encoding='utf-8')
        self.logger.info(f"Review saved to: {review_path}")
        
        if confidence_score >= self.config.get("confidence_threshold", 0.9):
            final_path = Path("specs/fe_spec_final.md")
            final_path.write_text(Path(fe_spec_path).read_text(encoding='utf-8'), encoding='utf-8')
            self.logger.info(f"Final specification saved to: {final_path}")
        
        return {
            "confidence_score": confidence_score,
            "review_path": str(review_path)
        }
    
    def _extract_confidence_score(self, response: str) -> float:
        match = re.search(r'CONFIDENCE_SCORE:\s*(\d+)%?', response, re.IGNORECASE)
        if match:
            return float(match.group(1)) / 100.0
        
        self.logger.warning("Could not extract confidence score, defaulting to 0.5")
        return 0.5

