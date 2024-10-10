# src/models/batch_job.py

from pydantic import BaseModel, Field, ConfigDict


class BatchJob(BaseModel):
    """Represents a batch job with its status and output information."""
    id: str = Field(..., description="Unique identifier for the batch job")
    status: str = Field(..., description="Current status of the batch job")
    output_file_id: str = Field(..., description="Identifier for the output file of the batch job")

    model_config = ConfigDict(frozen=True)
