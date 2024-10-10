# src/services/schema_service.py
import json
from pathlib import Path
from typing import Dict, Any

from pydantic import BaseModel, Field


class SchemaService(BaseModel):
    """Service for loading JSON schemas."""

    schema_file: Path = Field("./storage/schema.json")

    def load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema from a file."""
        try:
            with open(self.schema_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise ValueError(f"Schema file not found: {self.schema_file}")