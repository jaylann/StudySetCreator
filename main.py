import argparse
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.services.study_set_creator import StudySetCreator
from src.utils.config import get_api_key
from src.utils.logging import get_logger

logger = get_logger()

class CLIArguments(BaseModel):
    pdf_path: str = Field(..., description="Path to the PDF file")
    model: str = Field("gpt-4o-mini", description="OpenAI model to use")
    output: str = Field("study_set.csv", description="Output CSV file name")
    chunk_size: int = Field(10, description="Number of pages to process at once")
    use_batch: bool = Field(False, description="Use OpenAI Batch API for processing")
    text_only: bool = Field(False, description="Extract text only, ignore images")
    language: str = Field("english", description="Language for the study set")
    no_resume: bool = Field(False, description="Whether to resume processing from the last checkpoint. WARNING: If set and a progress file exists, it will be overwritten.")

def parse_arguments() -> CLIArguments:
    """Parse command-line arguments and return a CLIArguments object."""
    parser = argparse.ArgumentParser(
        description="Create a study set from a PDF file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Add standard and custom help options
    parser.add_argument("-?", action="help", help="Show this help message and exit.")

    # Define arguments
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file.")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model to use.")
    parser.add_argument("--output", type=str, default="study_set.csv", help="Output CSV file name.")
    parser.add_argument("--chunk_size", type=int, default=10, help="Number of pages to process at once.")
    parser.add_argument("--use_batch", action="store_true", help="Use OpenAI Batch API for processing.")
    parser.add_argument("--text_only", action="store_true", help="Extract text only, ignore images.")
    parser.add_argument("--language", type=str, default="english", help="Language for the study set.")
    parser.add_argument(
        "--no_resume",
        action="store_true",
        default=False,
        help="Whether to resume processing from the last checkpoint. WARNING: If set and a progress file exists, it will be overwritten."
    )

    args = parser.parse_args()
    return CLIArguments(**vars(args))

def main() -> None:
    """
    Main function to create a study set from a PDF file.

    This function parses command-line arguments, initializes the StudySetCreator,
    and generates the study set based on the provided PDF file and options.
    """
    args = parse_arguments()

    api_key = get_api_key()
    if not api_key:
        logger.error("API key not found. Please set it in the .env file.")
        return

    creator = StudySetCreator(
        api_key=api_key,
        model=args.model,
        output_csv=args.output,
        chunk_size=args.chunk_size,
        use_batch=args.use_batch,
        language=args.language,
        no_resume=args.no_resume
    )

    creator.to_study_set(args.pdf_path, args.text_only)

if __name__ == "__main__":
    main()
