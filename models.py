from typing import List
from pydantic import BaseModel


class ImageUploadModel(BaseModel):
    url: str


class ImageUploadAWBModel(BaseModel):
    url: str
    name: str
    phone: str
    address: List[str]
    awb_number: str
