# src/models/openai_response.py

from typing import List
from pydantic import BaseModel, Field, ConfigDict
from src.models.study_card import StudyCard


class OpenAIResponse(BaseModel):
    """
    Represents a response from the OpenAI API, including study cards.

    Attributes:
        study_cards (List[StudyCard]): List of study cards generated from the response.

    Example:
        >>> cards = [StudyCard(question="What is Python?", answer="A programming language")]
        >>> response = OpenAIResponse(study_cards=cards)
    """
    study_cards: List[StudyCard] = Field(..., description="List of study cards generated from the response")

    model_config = ConfigDict(frozen=True)