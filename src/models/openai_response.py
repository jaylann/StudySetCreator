# src/models/openai_response.py

from typing import List

from pydantic import BaseModel, Field, ConfigDict

from src.models.study_card import StudyCard


class OpenAIResponse(BaseModel):
    """Represents a response from the OpenAI API, including study cards."""
    study_cards: List[StudyCard] = Field(..., description="List of study cards generated from the response")

    model_config = ConfigDict(frozen=True)
