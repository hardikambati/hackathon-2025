from pydantic import BaseModel


class ImageUploadModel(BaseModel):
    url: str
