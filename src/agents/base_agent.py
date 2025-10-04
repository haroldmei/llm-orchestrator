"""Base class for all AI agents"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import anthropic
import openai
import logging


class BaseAgent(ABC):
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "deepseek")
        self.model = config.get("model", "deepseek-chat")
        
        if self.provider == "anthropic":
            self.api_key = config.get("anthropic_api_key")
            self.client = anthropic.Anthropic(api_key=self.api_key)
        elif self.provider == "deepseek":
            self.api_key = config.get("deepseek_api_key")
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url="https://api.deepseek.com"
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
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
        return self.call_llm(prompt, max_tokens)
    
    def call_llm(self, prompt: str, max_tokens: int = 4096) -> str:
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            elif self.provider == "deepseek":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error calling LLM API: {str(e)}")
            raise

