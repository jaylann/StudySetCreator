# src/utils/config.py

import os
from dotenv import load_dotenv

def get_api_key() -> str:
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')
