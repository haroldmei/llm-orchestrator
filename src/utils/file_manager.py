"""File management utilities"""
from pathlib import Path
from typing import Dict, Any
import shutil


class FileManager:
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data_dir = Path(config.get("data_dir", "data"))
        self.specs_dir = Path(config.get("specs_dir", "specs"))
        self.logs_dir = Path(config.get("logs_dir", "logs"))
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        self.data_dir.mkdir(exist_ok=True)
        self.specs_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def read_file(self, path: str) -> str:
        return Path(path).read_text(encoding='utf-8')
    
    def write_file(self, path: str, content: str):
        Path(path).write_text(content, encoding='utf-8')
    
    def copy_file(self, src: str, dst: str):
        shutil.copy(src, dst)
    
    def file_exists(self, path: str) -> bool:
        return Path(path).exists()

