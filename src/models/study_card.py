from pydantic import BaseModel, Field, ConfigDict


class StudyCard(BaseModel):
    """Represents a study card with a question and its corresponding answer."""
    question: str = Field(..., min_length=1, description="The question presented on the study card")
    answer: str = Field(..., min_length=1, description="The answer corresponding to the question on the study card")

    model_config = ConfigDict(frozen=True)
