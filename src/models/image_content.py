from pydantic import BaseModel, Field, ConfigDict

from src.models.image_source import ImageSource


class ImageContent(BaseModel):
    """Represents image content with its source information."""
    type: str = Field(default="image", description="Type of content")
    source: ImageSource = Field(..., description="Source information for the image")

    model_config = ConfigDict(frozen=True)
