# src/models/page_content.py

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class PageContent(BaseModel):
    """Represents the content of a page, including text and image data."""
    page_number: int = Field(..., ge=0, description="Page number")
    image_data: Optional[bytes] = Field(default=None, description="Binary image data")
    text: Optional[str] = Field(default=None, description="Text content of the page")

    model_config = ConfigDict(frozen=True)
