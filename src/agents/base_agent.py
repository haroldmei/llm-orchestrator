"""Base class for all AI agents"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import anthropic
import logging


class BaseAgent(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get("anthropic_api_key")
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = config.get("model", "claude-sonnet-4-20250514")
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        
        handler = logging.FileHandler(f"logs/{self.__class__.__name__.lower()}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        pass
    
    def call_claude(self, prompt: str, max_tokens: int = 4096) -> str:
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"Error calling Claude API: {str(e)}")
            raise

