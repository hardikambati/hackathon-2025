import os

# standard imports
from fastapi import (
    status,
    FastAPI,
    Depends,
)
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# 3rd party imports
from ultralytics import YOLO
from roboflow import Roboflow
from huggingface_hub import hf_hub_download

# internal imports
from models import (
    ImageUploadModel,
)
from signature_module.detect import (
    detect_signature,
)
from stamp_module.detect import (
    detect_stamp,
)
from dotenv import load_dotenv


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load signature model
    print("[Signature] Loading YOLO model...")
    signature_model_path = hf_hub_download(
        repo_id="tech4humans/yolov8s-signature-detector", 
        filename="yolov8s.pt"
    )
    app.state.signature_model = YOLO(signature_model_path)
    print("[Signature] Model loaded successfully")

    # load stamp model
    print("[Stamp] Loading Roboflow model...")
    rf = Roboflow(api_key=os.environ.get("ROBOFLOW_KEY"))
    project = rf.workspace().project("stamp-detection-okgih")
    stamp_model_path = project.version(1).model
    app.state.stamp_model = stamp_model_path
    print("[Stamp] Model loaded successfully")
    yield
    print("Shutting down")


app = FastAPI(
    lifespan=lifespan
)


def get_signature_model():
    return app.state.signature_model


def get_stamp_model():
    return app.state.stamp_model


@app.get("/")
def get_root():
    return JSONResponse(
        content={
            "message": "Server is up and running!"
        },
        status_code=status.HTTP_200_OK
    )


@app.post("/detect/signature")
def post_signature(image: ImageUploadModel, model = Depends(get_signature_model)):
    image_dict = image.model_dump()
    # TODO add url regex handling
    url = image_dict.get("url")
    if url:
        result, message = detect_signature(url=url, model=model)
        return JSONResponse(
            content={
                "status": result,
                "message": message
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "failed"
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )


@app.post("/detect/stamp")
def post_signature(image: ImageUploadModel, model = Depends(get_stamp_model)):
    image_dict = image.model_dump()
    # TODO add url regex handling
    url = image_dict.get("url")
    if url:
        result, message = detect_stamp(url=url, model=model)
        return JSONResponse(
            content={
                "status": result,
                "message": message
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "failed"
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )
