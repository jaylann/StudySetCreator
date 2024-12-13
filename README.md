# StudySetCreator

## Description

StudySetCreator is a Python tool that generates study sets (flashcards) from PDF files using OpenAI's language models. It processes the content of a PDF file, extracts text and images, and uses the OpenAI API to create question-answer pairs suitable for studying or revision purposes. The generated study set is saved as a CSV file, ready to be imported into flashcard applications or used directly.

## Features

- **PDF Processing**: Extracts text and images from PDF files.
- **OpenAI Integration**: Utilizes OpenAI's GPT models to generate study cards from the extracted content.
- **Batch Processing**: Supports processing in chunks to handle large PDF files efficiently.
- **Resume Capability**: Can resume processing from where it left off in case of interruptions.
- **Language Support**: Generates study sets in the specified language.
- **Customization**: Allows customization of various parameters like model selection, output file name, chunk size, etc.

## Prerequisites

- **Python**: Version 3.7 or higher.
- **OpenAI API Key**: Required to access OpenAI's language models.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/jaylann/StudySetCreator.git
   cd StudySetCreator
   ```

2. **Create a Virtual Environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Set Up the `.env` File

The application requires an OpenAI API key to function. This key should be stored in a `.env` file in the project's root directory.

1. **Create the `.env` File**

   There is a `.env.template` file provided in the project. Copy this template to create your `.env` file:

   ```bash
   cp .env.template .env
   ```

2. **Edit the `.env` File**

   Open the `.env` file in a text editor and add your OpenAI API key:

   ```dotenv
   OPENAI_API_KEY=your-openai-api-key-here
   ```

   Replace `your-openai-api-key-here` with your actual OpenAI API key.

## Usage

Run the `main.py` script with the required arguments to generate a study set from a PDF file.

```bash
python main.py [options]
```

### Optional Arguments

- `--model`: OpenAI model to use (default: `gpt-4o-mini`).
- `--output`: Output CSV file name (default: `study_set.csv`).
- `--input`: Input PDF file to process (required).
- `--in_dir`: Input directory containing PDF files to process.
- `--out_dir`: Output directory to save the study sets.
- `--chunk_size`: Number of pages to process at once (default: `10`).
- `--use_batch`: Use OpenAI Batch API for processing.
- `--text_only`: Extract text only, ignore images.
- `--language`: Language for the study set (default: `english`).
- `--no_resume`: Whether to resume processing from the last checkpoint. WARNING: If set and a progress file exists, it will be overwritten.

### Examples

1. **Basic Usage**

   Generate a study set from `document.pdf` using the default settings.

   ```bash
   python main.py --input document.pdf --output document.csv
   ```

2. **Specify Output File and Model**

   Generate a study set from `lecture_notes.pdf`, using the `gpt-4o` model, and save the output to `flashcards.csv`.

   ```bash
   python main.py --model gpt-4o --output flashcards.csv --input lecture_notes.pdf
   ```

3. **Process Only Text Content**

   Generate a study set ignoring images in the PDF.

   ```bash
   python main.py --text_only --input textbook.pdf --output textbook.csv
   ```

4. **Use Batch Processing**

   Use OpenAI's Batch API to process the PDF (suitable for large PDFs. Reduces cost by ~50% but may take longer).

   ```bash
   python main.py --use_batch --input large_document.pdf --output large_document.csv
   ```

5. **Specify Language**

   Generate a study set in Spanish.

   ```bash
   python main.py --language spanish --input notas_de_clase.pdf --output notas_de_clase.csv
   ```

## Customization

### Modifying the Prompt

The system prompt used by the OpenAI API can be customized to change how study cards are generated.

- **Prompt File**: `./storage/prompt.txt`

  Edit this file to modify the prompt. The placeholder `[LANGUAGE]` in the prompt will be replaced with the language specified via the `--language` argument.

### Modifying the Schema

The JSON schema defines the expected structure of the API responses.

- **Schema File**: `./storage/schema.json`

  Edit this file to change the schema if you need the responses in a different format.

## Logging

The application uses logging to provide information about its operation.

- **Log Output**: The application outputs logs to the console. You can modify the logging configuration in `src/utils/logging.py` if you need to change log levels or output formats.

## Error Handling

- **Resume Processing**: If the processing is interrupted, the application can resume from where it left off using the progress saved in `progress.json`.
- **Progress File**: The file `progress.json` is used to keep track of progress. It can be deleted to start processing from the beginning.
- **Batch Processing Errors**: If a batch job fails or is still in progress, an error message will be logged.

## Dependencies

All required Python packages are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Notes

- **API Usage**: Be mindful of your OpenAI API usage and billing.
- **Supported Models**: Ensure that the model you specify (e.g., `gpt-4`) is available to your OpenAI account.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs or feature requests.

## License

This project is licensed under the **MIT License**.

---

<p align="center">
  Made with ❤️ by <a href="https://lanfermann.dev">Justin Lanfermann</a>
</p>
