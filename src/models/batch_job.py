# src/models/batch_job.py

from pydantic import BaseModel, Field, ConfigDict, field_validator

from src.models.job_status import JobStatus


class BatchJob(BaseModel):
    """
    Represents a batch job with its status and output information.

    Attributes:
        id (str): Unique identifier for the batch job.
        status (str): Current status of the batch job.
        output_file_id (str): Identifier for the output file of the batch job.

    Example:
        >>> job = BatchJob(id="job123", status="running", output_file_id="file456")
    """
    id: str = Field(..., description="Unique identifier for the batch job")
    status: str = Field(..., description="Current status of the batch job")
    output_file_id: str = Field(..., description="Identifier for the output file of the batch job")

    model_config = ConfigDict(frozen=True)

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in JobStatus._value2member_map_:
            raise ValueError(f"Invalid status. Must be one of {list(JobStatus)}")
        return v
