# src/models/batch_result.py

from typing import Dict
from pydantic import BaseModel, Field, ConfigDict, field_validator


class BatchResult(BaseModel):
    """
    Represents the result of a batch operation.

    Attributes:
        custom_id (str): Custom identifier for the batch result.
        response (Dict): Response data for the batch result.

    Example:
        >>> result = BatchResult(custom_id="batch001", response={"status": "success", "items": 100})
    """
    custom_id: str = Field(..., description="Custom identifier for the batch result")
    response: Dict = Field(..., description="Response data for the batch result")

    model_config = ConfigDict(frozen=True)

    @field_validator("custom_id")
    @classmethod
    def custom_id_not_empty(cls, v):
        if not v.strip():
            raise ValueError("custom_id must not be empty")
        return v