# src/services/openai_service.py
from typing import List

from src.models import OpenAIResponse
from src.models.page_content import PageContent
from src.services.openai_base_service import OpenAIBaseService


class OpenAIDirectService(OpenAIBaseService):
    """Service for direct OpenAI API calls."""

    def generate_study_cards(self, pages: List[PageContent], batch_size: int = 10, language:str="english") -> OpenAIResponse:
        cards = []
        system_prompt = self.prompt_service.load_prompt(language)
        json_schema = self.schema_service.load_schema()

        for batch in self.batch_iterator(pages, batch_size):
            content = [self.prepare_content(page) for page in batch]
            messages = [{"role": "system", "content": [{
                "type": "text",
                "text": system_prompt
            }]}] + [{"role": "user", "content": content}]

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=1,
                    max_tokens=4095,
                    response_format=json_schema
                )
                study_cards = OpenAIResponse.model_validate_json(response.choices[0].message.content)
                cards.extend(study_cards.study_cards)
            except Exception as e:
                self.logger.error(f"Error generating study cards: {e}")

        return OpenAIResponse(study_cards=cards)