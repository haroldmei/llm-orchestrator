"""Robust Feature Engineering Reviewer with multiple extraction strategies"""
from pathlib import Path
from typing import Dict, Any, Optional
import re
from src.agents.base_agent import BaseAgent


class FEReviewerRobust(BaseAgent):
    
    def get_prompt_template(self) -> str:
        prompt_path = Path("prompts/dl_fe_reviewer.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        return ""
    
    def _extract_confidence_score(self, response: str) -> Optional[float]:
        """Try multiple strategies to extract confidence score"""
        
        # Strategy 1: Exact format "CONFIDENCE_SCORE: XX%"
        patterns = [
            r'CONFIDENCE[_\s-]*SCORE[:\s]*(\d+)%?',
            r'confidence[:\s]+(\d+)%',
            r'score[:\s]+(\d+)%',
            r'(\d+)%\s+confidence',
            r'confident[:\s]+(\d+)%',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                if 0 <= score <= 100:
                    self.logger.info(f"Extracted confidence score: {score}% using pattern: {pattern}")
                    return score / 100.0
                else:
                    self.logger.warning(f"Found score {score} but out of valid range (0-100)")
        
        # Strategy 2: Look for standalone percentage in last paragraph
        paragraphs = response.strip().split('\n\n')
        if paragraphs:
            last_para = paragraphs[-1]
            match = re.search(r'\b(\d{1,3})%\b', last_para)
            if match:
                score = int(match.group(1))
                if 0 <= score <= 100:
                    self.logger.info(f"Extracted score from last paragraph: {score}%")
                    return score / 100.0
        
        return None
    
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

IMPORTANT: You MUST include the confidence score in this exact format on its own line:
CONFIDENCE_SCORE: XX%

Where XX is a number from 0 to 100."""
        
        response = self.call_claude(prompt)
        
        confidence_score = self._extract_confidence_score(response)
        
        if confidence_score is None:
            self.logger.error(f"Failed to extract confidence score from response. First 500 chars: {response[:500]}")
            # Re-ask Claude specifically for the score
            retry_prompt = f"""Based on your previous review, what is your confidence score (0-100%) 
that the feature specification can successfully implement the data specification?

Reply ONLY with: CONFIDENCE_SCORE: XX%"""
            
            try:
                retry_response = self.call_claude(retry_prompt)
                confidence_score = self._extract_confidence_score(retry_response)
            except Exception as e:
                self.logger.error(f"Retry failed: {str(e)}")
            
            if confidence_score is None:
                self.logger.warning("All extraction attempts failed, defaulting to 0.5")
                confidence_score = 0.5
        
        review_path = Path("specs/fe_spec_review.md")
        review_path.write_text(response, encoding='utf-8')
        self.logger.info(f"Review saved with confidence: {confidence_score:.0%}")
        
        if confidence_score >= self.config.get("confidence_threshold", 0.9):
            final_path = Path("specs/fe_spec_final.md")
            final_path.write_text(Path(fe_spec_path).read_text(encoding='utf-8'), encoding='utf-8')
            self.logger.info(f"Final specification saved to: {final_path}")
        
        return {
            "confidence_score": confidence_score,
            "review_path": str(review_path)
        }

