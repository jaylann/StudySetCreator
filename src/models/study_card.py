# src/models/study_card.py

from pydantic import BaseModel, Field, ConfigDict, field_validator


class StudyCard(BaseModel):
    """
    Represents a study card with a question and its corresponding answer.

    Attributes:
        question (str): The question presented on the study card.
        answer (str): The answer corresponding to the question on the study card.

    Example:
        >>> card = StudyCard(question="What is the capital of France?", answer="Paris")
    """
    question: str = Field(..., min_length=1, description="The question presented on the study card")
    answer: str = Field(..., min_length=1, description="The answer corresponding to the question on the study card")

    model_config = ConfigDict(frozen=True)

    @field_validator("question", "answer")
    @classmethod
    def check_content(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Question and answer must be at least 3 characters long (excluding whitespace)")
        return v