# src/services/study_set_creator.py

import csv
import json
import os
from typing import List

from pydantic import BaseModel

from src.models import OpenAIResponse
from src.models.page_content import PageContent
from src.services.openai_base_service import OpenAIBaseService
from src.services.openai_batch_service import OpenAIBatchService
from src.services.openai_direct_service import OpenAIDirectService
from src.services.pdf_processor import PDFProcessor
from src.services.prompt_service import PromptService
from src.services.schema_service import SchemaService
from src.utils.logging import get_logger
from src.utils.progress import get_progress_bar


class Progress(BaseModel):
    progress: int = 0
    batch_job_id: str | None = None


class StudySetCreator:
    """
    A class to create study sets from PDF files using OpenAI services.
    """

    def __init__(
            self,
            api_key: str,
            model: str,
            output_csv: str,
            chunk_size: int = 10,
            use_batch: bool = False,
            language: str = "english"
    ):
        self.pdf_processor = PDFProcessor()
        self.output_csv = output_csv
        self.logger = get_logger()
        self.chunk_size = chunk_size
        self.use_batch = use_batch
        self.progress_file = 'progress.json'
        self.language = language
        self.prompt_service = PromptService()
        self.schema_service = SchemaService()

        self.api_service: OpenAIBaseService = (
            OpenAIBatchService(api_key=api_key, model=model, prompt_service=self.prompt_service, schema_service=self.schema_service) if use_batch
            else OpenAIDirectService(api_key=api_key, model=model, prompt_service=self.prompt_service, schema_service=self.schema_service)
        )

    def to_study_set(self, pdf_path: str, text_only: bool = False):
        """
        Process a PDF file and create a study set.

        Args:
            pdf_path (str): Path to the PDF file.
            text_only (bool): If True, process only text content from the PDF.
        """
        self.logger.info(f"Processing PDF: {pdf_path}")
        pages_content = self.pdf_processor.process_pdf(pdf_path, text_only)

        if self.use_batch:
            self._process_with_batch_api(pages_content)
        else:
            self._process_with_openai_api(pages_content)

    def _process_with_openai_api(self, pages_content: List[PageContent]):
        """
        Process pages content using OpenAI API directly.

        Args:
            pages_content (List[PageContent]): List of page contents to process.
        """
        self.logger.info("Generating study cards using OpenAI API")
        all_study_cards = []
        progress = self._load_progress()

        for i in get_progress_bar(range(progress.progress, len(pages_content), self.chunk_size), desc="Processing pages"):
            chunk = pages_content[i:i + self.chunk_size]
            try:
                response = self.api_service.generate_study_cards(chunk, language=self.language)
                all_study_cards.extend(response.study_cards)
                self._save_progress(Progress(progress=i + self.chunk_size))
            except Exception as e:
                self.logger.error(f"Error processing chunk starting at page {i}: {e}")

        self._save_csv(all_study_cards)

    def _process_with_batch_api(self, pages_content: List[PageContent]):
        """
        Process pages content using OpenAI Batch API.

        Args:
            pages_content (List[PageContent]): List of page contents to process.
        """
        self.logger.info("Generating study cards using OpenAI Batch API")
        progress = self._load_progress()

        if progress.batch_job_id:
            self.logger.info(f"Resuming batch job with ID: {progress.batch_job_id}")
            batch_result = self.api_service.retrieve_batch_results(progress.batch_job_id)
        else:
            batch_job_id = self.api_service.create_batch_job(pages_content, self.chunk_size, language=self.language)
            self._save_progress(Progress(batch_job_id=batch_job_id))
            batch_result = self.api_service.retrieve_batch_results(batch_job_id)

        if batch_result:
            all_study_cards = self.api_service.parse_batch_results(batch_result)
            self._save_csv(all_study_cards.study_cards)
            self._clear_progress()
        else:
            self.logger.error("Batch processing failed or is still in progress.")

    def _save_csv(self, study_cards: List[OpenAIResponse]):
        """
        Save study cards to a CSV file.

        Args:
            study_cards (List[OpenAIResponse]): List of study cards to save.
        """
        with open(self.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Question', 'Answer']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            for card in study_cards:
                writer.writerow({'Question': card.question, 'Answer': card.answer})

        self.logger.info(f"Study set saved to {self.output_csv}")

    def _load_progress(self) -> Progress:
        """
        Load progress from the progress file.

        Returns:
            Progress: The loaded progress.
        """
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                return Progress.model_validate_json(f.read())
        return Progress()

    def _save_progress(self, progress: Progress):
        """
        Save progress to the progress file.

        Args:
            progress (Progress): The progress to save.
        """
        with open(self.progress_file, 'w') as f:
            f.write(progress.model_dump_json())

    def _clear_progress(self):
        """Remove the progress file."""
        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)