from pydantic import BaseModel, Field, ConfigDict


class ImageSource(BaseModel):
    """Represents the source of an image, including its encoding and data."""
    type: str = Field(default="base64", description="Type of image source")
    media_type: str = Field(default="image/png", description="MIME type of the image")
    data: str = Field(..., description="Base64 encoded image data")

    model_config = ConfigDict(frozen=True)
