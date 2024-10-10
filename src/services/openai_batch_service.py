# src/services/batch_service.py
import json
import time
from typing import List, Dict, Any

from src.models.openai_response import OpenAIResponse
from src.models.page_content import PageContent
from src.services.openai_base_service import OpenAIBaseService


class OpenAIBatchService(OpenAIBaseService):
    """Service for batch processing using OpenAI API."""

    batch_file_name: str = "batch_tasks.jsonl"
    results_file_name: str = "batch_output.jsonl"

    def generate_study_cards(self, pages: List[PageContent], batch_size: int = 10 , language:str = "english") -> OpenAIResponse:
        batch_job_id = self.create_batch_job(pages, batch_size, language)
        batch_results = self.retrieve_batch_results(batch_job_id)
        return self.parse_batch_results(batch_results)

    def create_batch_job(self, pages: List[PageContent], batch_size: int = 10, language:str = "english") -> str:
        self.logger.info("Creating batch file for processing")
        tasks = []

        system_prompt = self.prompt_service.load_prompt(language)
        json_schema = self.schema_service.load_schema()

        for index, batch in enumerate(self.batch_iterator(pages, batch_size)):
            batch_content = [self.prepare_content(page) for page in batch]
            task = {
                "custom_id": f"task-{index}",
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": self.model,
                    "temperature": 1,
                    "messages":[{"role": "system", "content": [{
                        "type": "text",
                        "text": system_prompt
                    }]},{"role": "user", "content": batch_content}],
                    "max_tokens": 4095,
                    "response_format": json_schema
                }
            }
            tasks.append(task)

        with open(self.batch_file_name, 'w') as file:
            for task in tasks:
                file.write(json.dumps(task) + '\n')

        batch_file = self.client.files.create(file=open(self.batch_file_name, "rb"), purpose="batch")
        self.logger.info(f"Batch file uploaded with ID: {batch_file.id}")

        batch_job = self.client.batches.create(input_file_id=batch_file.id, endpoint="/v1/chat/completions", completion_window="24h")
        self.logger.info(f"Batch job created with ID: {batch_job.id}")
        return batch_job.id

    def retrieve_batch_results(self, batch_job_id: str) -> List[Dict[str, Any]]:
        self.logger.info("Checking batch job status...")
        batch_job = self.client.batches.retrieve(batch_job_id)

        while batch_job.status != 'completed':
            self.logger.info(f"Batch job status: {batch_job.status}. Waiting for completion...")
            time.sleep(10)
            batch_job = self.client.batches.retrieve(batch_job_id)

        self.logger.info("Batch job completed. Retrieving results...")
        result_file_id = batch_job.output_file_id
        result_content = self.client.files.content(result_file_id).text

        with open(self.results_file_name, 'w') as file:
            file.write(result_content)

        return self._load_results()

    def _load_results(self) -> List[Dict[str, Any]]:
        results = []
        with open(self.results_file_name, 'r') as file:
            for line in file:
                results.append(json.loads(line.strip()))
        return results

    def parse_batch_results(self, batch_results: List[Dict[str, Any]]) -> OpenAIResponse:
        all_study_cards = []
        for res in batch_results:
            try:
                result_content = res['response']['body']['choices'][0]['message']['content']
                study_cards = OpenAIResponse.model_validate_json(result_content)
                all_study_cards.extend(study_cards.study_cards)
            except Exception as e:
                self.logger.error(f"Error parsing result for task {res.get('custom_id', 'unknown')}: {e}")
        return OpenAIResponse(study_cards=all_study_cards)

