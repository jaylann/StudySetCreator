# src/services/prompt_service.py
from pathlib import Path
from typing import List, Dict, Any

from pydantic import BaseModel, Field


class PromptService(BaseModel):
    """Service for loading and modifying system prompts."""

    prompt_file: Path = Field("./storage/prompt.txt")

    def load_prompt(self, language:str) -> str:
        """Load the system prompt from a file."""
        try:
            with open(self.prompt_file, 'r') as file:
                return file.read().strip().replace("[LANGUAGE]", language)
        except FileNotFoundError:
            raise ValueError(f"Prompt file not found: {self.prompt_file}")

    def modify_prompt(self, prompt: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Modify the system prompt if needed."""
        # Implement any prompt modification logic here
        return prompt
