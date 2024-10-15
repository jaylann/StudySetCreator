# src/models/openai_request.py

from typing import List, Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator


class OpenAIRequest(BaseModel):
    """
    Represents a request to the OpenAI API.

    Attributes:
        model (str): The model to use for the request.
        messages (List[Dict]): List of message dictionaries for the conversation.
        temperature (float): Sampling temperature, defaults to 0.
        max_tokens (int): Maximum number of tokens to generate, defaults to 4095.
        top_p (float): Nucleus sampling parameter, defaults to 1.
        frequency_penalty (float): Frequency penalty parameter, defaults to 0.
        presence_penalty (float): Presence penalty parameter, defaults to 0.
        response_format (Dict): Desired response format, defaults to an empty dict.

    Example:
        >>> request = OpenAIRequest(
        ...     model="gpt-3.5-turbo",
        ...     messages=[{"role": "user", "content": "Hello, AI!"}],
        ...     temperature=0.7
        ... )
    """
    model: str = Field(..., description="The model to use for the request")
    messages: List[Dict] = Field(..., description="List of message dictionaries for the conversation")
    temperature: float = Field(default=0, ge=0, le=2, description="Sampling temperature")
    max_tokens: int = Field(default=4095, gt=0, description="Maximum number of tokens to generate")
    top_p: float = Field(default=1, ge=0, le=1, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0, ge=-2, le=2, description="Frequency penalty parameter")
    presence_penalty: float = Field(default=0, ge=-2, le=2, description="Presence penalty parameter")
    response_format: Dict = Field(default={}, description="Desired response format")

    model_config = ConfigDict(frozen=True)

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v):
        if not v:
            raise ValueError("Messages list cannot be empty")
        return v
