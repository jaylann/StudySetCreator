# src/models/image_content.py

from pydantic import BaseModel, Field, ConfigDict
from src.models.image_source import ImageSource


class ImageContent(BaseModel):
    """
    Represents image content with its source information.

    Attributes:
        type (str): Type of content, defaults to "image".
        source (ImageSource): Source information for the image.

    Example:
        >>> source = ImageSource(data="base64_encoded_data")
        >>> content = ImageContent(source=source)
    """
    type: str = Field(default="image", description="Type of content")
    source: ImageSource = Field(..., description="Source information for the image")

    model_config = ConfigDict(frozen=True)