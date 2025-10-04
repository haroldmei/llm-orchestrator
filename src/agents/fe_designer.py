"""Feature Engineering Designer Agent"""
from pathlib import Path
from typing import Any
from src.agents.base_agent import BaseAgent


class FEDesigner(BaseAgent):
    
    def get_prompt_template(self) -> str:
        prompt_path = Path("prompts/dl_fe_designer.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding='utf-8')
        return ""
    
    def execute(self, data_spec_path: str) -> str:
        self.logger.info(f"Designing features from: {data_spec_path}")
        
        data_spec = Path(data_spec_path).read_text(encoding='utf-8')
        prompt_template = self.get_prompt_template()
        
        prompt = f"""{prompt_template}

# Data Specification
{data_spec}

Please design features for a BiLSTM model following industry best practices. Output the feature specification."""
        
        response = self.call_claude(prompt)
        
        output_path = Path("specs/fe_spec.md")
        output_path.write_text(response, encoding='utf-8')
        self.logger.info(f"Feature specification saved to: {output_path}")
        
        return str(output_path)

