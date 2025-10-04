"""Improved Feature Engineering Reviewer with structured output"""
from pathlib import Path
from typing import Dict, Any
import json
from src.agents.base_agent import BaseAgent


class FEReviewerImproved(BaseAgent):
    
    def get_prompt_template(self) -> str:
        """Not used in structured approach but required by base"""
        return ""
    
    def call_claude_structured(self, prompt: str) -> Dict[str, Any]:
        """Call LLM and request structured JSON output"""
        system_prompt = """You must respond with valid JSON matching this schema:
{
  "summary": "Overall assessment",
  "detailed_review": "Detailed analysis",
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"],
  "confidence_score": 85
}
The confidence_score must be an integer between 0 and 100."""

        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = response.content[0].text
            elif self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model,
                    max_tokens=4096,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                )
                response_text = response.choices[0].message.content
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
            
            # Try to extract JSON if wrapped in markdown
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            
            result = json.loads(response_text)
            
            # Validate confidence score
            if "confidence_score" not in result:
                raise ValueError("Missing confidence_score in response")
            
            score = result["confidence_score"]
            if not isinstance(score, (int, float)) or not (0 <= score <= 100):
                raise ValueError(f"Invalid confidence_score: {score}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Structured output failed: {str(e)}")
            raise
    
    def execute(self, fe_spec_path: str, data_spec_path: str) -> Dict[str, Any]:
        self.logger.info(f"Reviewing feature specification: {fe_spec_path}")
        
        fe_spec = Path(fe_spec_path).read_text(encoding='utf-8')
        data_spec = Path(data_spec_path).read_text(encoding='utf-8')
        
        prompt = f"""Review this feature specification against the data specification.

# Original Data Specification
{data_spec}

# Feature Specification to Review
{fe_spec}

Evaluate: completeness, technical correctness, BiLSTM suitability, best practices, 
implementation feasibility, edge cases, and performance.

Provide a confidence score (0-100) indicating how well this specification can implement 
the original data specification. 90+ means production-ready."""

        result = self.call_claude_structured(prompt)
        
        # Save formatted review
        review_text = f"""# Feature Specification Review

## Summary
{result['summary']}

## Detailed Review
{result['detailed_review']}

## Strengths
{chr(10).join('- ' + s for s in result['strengths'])}

## Areas for Improvement
{chr(10).join('- ' + i for i in result['improvements'])}

## Confidence Score
{result['confidence_score']}%
"""
        
        review_path = Path("specs/fe_spec_review.md")
        review_path.write_text(review_text, encoding='utf-8')
        self.logger.info(f"Review saved with confidence: {result['confidence_score']}%")
        
        confidence = result['confidence_score'] / 100.0
        
        if confidence >= self.config.get("confidence_threshold", 0.9):
            final_path = Path("specs/fe_spec_final.md")
            final_path.write_text(Path(fe_spec_path).read_text(encoding='utf-8'), encoding='utf-8')
            self.logger.info(f"Final specification saved to: {final_path}")
        
        return {
            "confidence_score": confidence,
            "review_path": str(review_path),
            "review_details": result
        }

