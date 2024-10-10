# src/services/openai_base_service.py
import abc
import base64
from itertools import islice
from typing import List, Dict, Any

from openai import OpenAI
from pydantic import BaseModel, Field

from src.models import OpenAIResponse
from src.models.page_content import PageContent
from src.services.prompt_service import PromptService
from src.services.schema_service import SchemaService
from src.utils.logging import get_logger


class OpenAIBaseService(BaseModel, abc.ABC):
    """Abstract base class for OpenAI services."""

    api_key: str
    model: str
    client: OpenAI = Field(default=None, init=False)
    logger: Any = Field(default=None, init=False)
    prompt_service: PromptService
    schema_service: SchemaService

    def __init__(self, **data):
        super().__init__(**data)
        self.client = OpenAI(api_key=self.api_key)
        self.logger = get_logger()

    @staticmethod
    def batch_iterator(iterable: List[Any], size: int):
        """Yield successive batches of specified size from iterable."""
        it = iter(iterable)
        while batch := list(islice(it, size)):
            yield batch

    def prepare_content(self, page: PageContent) -> Dict[str, Any]:
        """Prepare content for OpenAI API."""
        if page.image_data:
            image_base64 = base64.b64encode(page.image_data).decode('utf-8')
            return {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"}
            }
        return {"type": "text", "text": page.text or ""}

    @abc.abstractmethod
    def generate_study_cards(self, pages: List[PageContent], batch_size: int = 10, language:str = "english") -> OpenAIResponse:
        """Generate study cards from page content."""
        pass

    class Config:
        arbitrary_types_allowed=True