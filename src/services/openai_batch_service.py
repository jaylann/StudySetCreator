# src/services/openai_batch_service.py
import csv
import json
import time
from typing import List, Dict, Any, Optional

from src.models.openai_response import OpenAIResponse
from src.models.page_content import PageContent
from src.services.openai_base_service import OpenAIBaseService


class OpenAIBatchService(OpenAIBaseService):
    """Service for batch processing using OpenAI API."""

    batch_file_name: str = "batch_tasks.jsonl"
    results_file_name: str = "batch_output.jsonl"

    def generate_study_cards(self, pages: List[PageContent], batch_size: int = 10,
                             language: str = "english") -> OpenAIResponse:
        batch_job_id = self.create_batch_job(pages, batch_size, language)
        batch_results = self.retrieve_batch_results(batch_job_id)
        return self.parse_batch_results(batch_results)

    def create_batch_job(self, pages: List[PageContent], batch_size: int = 10, language: str = "english",
                         pdf_mapping: Optional[Dict[str, str]] = None) -> str:
        self.logger.info("Creating batch file for processing")
        tasks = []

        system_prompt = self.prompt_service.load_prompt(language)
        json_schema = self.schema_service.load_schema()

        for index, page in enumerate(pages):
            batch_content = [self.prepare_content(page)]
            if pdf_mapping:
                # Use the custom_id from pdf_mapping
                custom_id = list(pdf_mapping.keys())[index]
            else:
                custom_id = f"task-{index}"

            task = {
                "custom_id": custom_id,
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "model": self.model,
                    "temperature": 1,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": batch_content}
                    ],
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

        batch_job = self.client.batches.create(input_file_id=batch_file.id, endpoint="/v1/chat/completions",
                                               completion_window="24h")
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

    # src/services/openai_batch_service.py

    def parse_batch_results_with_mapping(self, batch_results: List[Dict[str, Any]], pdf_mapping: Dict[str, str]):
        """
        Parse batch results and save study cards to their respective CSV files based on mapping.

        Args:
            batch_results (List[Dict[str, Any]]): List of batch result dictionaries.
            pdf_mapping (Dict[str, str]): Mapping from custom_id to output CSV path.
        """
        study_cards_per_file = {}

        for res in batch_results:
            try:
                custom_id = res.get('custom_id')
                if not custom_id:
                    self.logger.error("Missing custom_id in batch result.")
                    continue
                result_content = res['response']['body']['choices'][0]['message']['content']
                study_cards = OpenAIResponse.model_validate_json(result_content).study_cards

                output_csv = pdf_mapping.get(custom_id)
                if not output_csv:
                    self.logger.error(f"No mapping found for custom_id: {custom_id}")
                    continue

                if output_csv not in study_cards_per_file:
                    study_cards_per_file[output_csv] = []
                study_cards_per_file[output_csv].extend(study_cards)
            except Exception as e:
                self.logger.error(f"Error processing batch result for custom_id {custom_id}: {e}")

        # Save study cards to their respective CSV files
        for output_csv, study_cards in study_cards_per_file.items():
            self._save_csv(study_cards, output_csv)
            self.logger.info(f"Study set saved to {output_csv}")

    def _save_csv(self, study_cards: List[OpenAIResponse], output_csv: str):
        """
        Save study cards to a CSV file.

        Args:
            study_cards (List[OpenAIResponse]): List of study cards to save.
            output_csv (str): Path to the output CSV file.
        """
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Question', 'Answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for card in study_cards:
                writer.writerow({'Question': card.question, 'Answer': card.answer})
