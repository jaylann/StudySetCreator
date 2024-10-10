# src/models/openai_request.py

from typing import List, Dict

from pydantic import BaseModel, Field, ConfigDict


class OpenAIRequest(BaseModel):
    """Represents a request to the OpenAI API."""
    model: str = Field(..., description="The model to use for the request")
    messages: List[Dict] = Field(..., description="List of message dictionaries for the conversation")
    temperature: float = Field(default=0, ge=0, le=2, description="Sampling temperature")
    max_tokens: int = Field(default=4095, gt=0, description="Maximum number of tokens to generate")
    top_p: float = Field(default=1, ge=0, le=1, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0, ge=-2, le=2, description="Frequency penalty parameter")
    presence_penalty: float = Field(default=0, ge=-2, le=2, description="Presence penalty parameter")
    response_format: Dict = Field(default={}, description="Desired response format")

    model_config = ConfigDict(frozen=True)
