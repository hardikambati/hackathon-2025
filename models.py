from pydantic import BaseModel


class ImageUploadModel(BaseModel):
    url: str

class ImageUploadAWBModel(BaseModel):
    url: str
    awb_number: str
