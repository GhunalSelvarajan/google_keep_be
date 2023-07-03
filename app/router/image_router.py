from fastapi import APIRouter, UploadFile
from firebase_admin.exceptions import FirebaseError, InternalError, UnknownError

from app.constants import DEFAULT_ROUTER_SETTINGS
from app.controller import ImageController
from app.model import CommonResponseModel
from app.utils import logger

image_router: APIRouter = APIRouter(
    tags=["Image"],
)


@image_router.post("/upload", name="Upload an image", **DEFAULT_ROUTER_SETTINGS)
def upload_image(file: UploadFile) -> CommonResponseModel:
    try:
        response: CommonResponseModel = ImageController.upload(file)
        return response
    except (FirebaseError, UnknownError, InternalError) as firebase_error:
        logger.error(
            f"Error while uploading image: {firebase_error}",
        )
        return CommonResponseModel(
            status="failure",
            message=f"Error while uploading image: {firebase_error}",
            error=str(firebase_error),
        )
