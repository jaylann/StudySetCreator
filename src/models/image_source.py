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


# src/models/image_source.py

import base64
from pydantic import BaseModel, Field, ConfigDict, field_validator


class ImageSource(BaseModel):
    """
    Represents the source of an image, including its encoding and data.

    Attributes:
        type (str): Type of image source, defaults to "base64".
        media_type (str): MIME type of the image, defaults to "image/png".
        data (str): Base64 encoded image data.

    Example:
        >>> source = ImageSource(data="base64_encoded_image_data")
    """
    type: str = Field(default="base64", description="Type of image source")
    media_type: str = Field(default="image/png", description="MIME type of the image")
    data: str = Field(..., description="Base64 encoded image data")

    model_config = ConfigDict(frozen=True)

    @field_validator("data")
    @classmethod
    def validate_base64(cls, v):
        try:
            base64.b64decode(v)
        except:
            raise ValueError("Invalid base64 encoded data")
        return v