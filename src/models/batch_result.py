from typing import Dict

from pydantic import BaseModel, Field, ConfigDict


class BatchResult(BaseModel):
    """Represents the result of a batch operation."""
    custom_id: str = Field(..., description="Custom identifier for the batch result")
    response: Dict = Field(..., description="Response data for the batch result")

    model_config = ConfigDict(frozen=True)
