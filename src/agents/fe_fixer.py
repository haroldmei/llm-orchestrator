"""Feature Engineering Fixer Agent"""
from pathlib import Path
from typing import Any
from src.agents.base_agent import BaseAgent


class FEFixer(BaseAgent):
    
    def get_prompt_template(self) -> str:
        prompt_path = Path("prompts/dl_fe_review_fixer.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        return ""
    
    def execute(self, fe_spec_path: str, review_path: str, data_spec_path: str) -> str:
        self.logger.info(f"Fixing feature specification based on review")
        
        fe_spec = Path(fe_spec_path).read_text(encoding='utf-8')
        review = Path(review_path).read_text(encoding='utf-8')
        data_spec = Path(data_spec_path).read_text(encoding='utf-8')
        prompt_template = self.get_prompt_template()
        
        prompt = f"""{prompt_template}

# Original Data Specification
{data_spec}

# Current Feature Specification
{fe_spec}

# Review Comments
{review}

Please fix the feature specification based on the review comments, following industry best practices."""
        
        response = self.call_claude(prompt)
        
        output_path = Path("specs/fe_spec_review_fixer.md")
        output_path.write_text(response, encoding='utf-8')
        self.logger.info(f"Updated feature specification saved to: {output_path}")
        
        return str(output_path)

