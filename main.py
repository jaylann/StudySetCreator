# src/cli.py

import argparse
import os
from typing import Optional

from pydantic import BaseModel, Field

from src.services.study_set_creator import StudySetCreator
from src.utils.config import get_api_key
from src.utils.logging import get_logger

logger = get_logger()


class CLIArguments(BaseModel):
    input: Optional[str] = Field(None, description="Path to the PDF file")
    output: Optional[str] = Field(None, description="Output CSV file name")
    in_dir: Optional[str] = Field(None, description="Path to the input directory containing PDF files")
    out_dir: Optional[str] = Field(None, description="Path to the output directory where CSV files will be saved")
    model: str = Field("gpt-4o-mini", description="OpenAI model to use")
    chunk_size: int = Field(10, description="Number of pages to process at once")
    use_batch: bool = Field(False, description="Use OpenAI Batch API for processing")
    text_only: bool = Field(False, description="Extract text only, ignore images")
    language: str = Field("english", description="Language for the study set")
    no_resume: bool = Field(False,
                            description="Whether to resume processing from the last checkpoint. WARNING: If set and a progress file exists, it will be overwritten.")


def parse_arguments() -> CLIArguments:
    """Parse command-line arguments and return a CLIArguments object."""
    parser = argparse.ArgumentParser(
        description="Create a study set from a PDF file or directory of PDFs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Define arguments
    parser.add_argument("--input", type=str, help="Path to the PDF file.")
    parser.add_argument("--output", type=str, help="Output CSV file name.")
    parser.add_argument("--in_dir", type=str, help="Path to the input directory containing PDF files.")
    parser.add_argument("--out_dir", type=str, help="Path to the output directory where CSV files will be saved.")
    parser.add_argument("--model", type=str, default="gpt-4o-mini", help="OpenAI model to use.")
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

    # Argument validation
    if (args.input is not None) != (args.output is not None):
        parser.error("Both --input and --output must be provided together.")

    if (args.in_dir is not None) != (args.out_dir is not None):
        parser.error("Both --in_dir and --out_dir must be provided together.")

    if (args.input and args.output) and (args.in_dir and args.out_dir):
        parser.error("Cannot use both --input/--output and --in_dir/--out_dir at the same time.")

    if not ((args.input and args.output) or (args.in_dir and args.out_dir)):
        parser.error("You must provide either both --input and --output, or both --in_dir and --out_dir.")

    return CLIArguments(**vars(args))


def main() -> None:
    """
    Main function to create a study set from a PDF file or directory of PDFs.

    This function parses command-line arguments, initializes the StudySetCreator,
    and generates the study set based on the provided PDF file(s) and options.
    """
    args = parse_arguments()

    api_key = get_api_key()
    if not api_key:
        logger.error("API key not found. Please set it in the .env file.")
        return

    if args.input:
        # Single file processing
        creator = StudySetCreator(
            api_key=api_key,
            model=args.model,
            output_csv=args.output,
            chunk_size=args.chunk_size,
            use_batch=args.use_batch,
            language=args.language,
            no_resume=args.no_resume
        )
        creator.to_study_set(args.input, args.text_only)
    elif args.in_dir:
        # Multiple files processing
        os.makedirs(args.out_dir, exist_ok=True)
        pdf_files = [f for f in os.listdir(args.in_dir) if f.lower().endswith('.pdf')]
        if not pdf_files:
            logger.error(f"No PDF files found in directory {args.in_dir}")
            return

        pdf_paths = [os.path.join(args.in_dir, pdf_file) for pdf_file in pdf_files]
        output_paths = [os.path.join(args.out_dir, os.path.splitext(pdf_file)[0] + '.csv') for pdf_file in pdf_files]

        creator = StudySetCreator(
            api_key=api_key,
            model=args.model,
            chunk_size=args.chunk_size,
            use_batch=args.use_batch,
            language=args.language,
            no_resume=args.no_resume
        )

        creator.process_multiple_pdfs(
            pdf_paths=pdf_paths,
            output_paths=output_paths,
            text_only=args.text_only
        )
    else:
        # Should not reach here
        logger.error("Invalid arguments provided.")
        return


if __name__ == "__main__":
    main()
