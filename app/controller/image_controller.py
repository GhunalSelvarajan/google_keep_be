from fastapi import UploadFile
from firebase_admin import storage
from firebase_admin.exceptions import FirebaseError, InternalError, UnknownError

from app.model import CommonResponseModel
from app.utils import logger


class ImageController:
    @staticmethod
    def upload(file: UploadFile) -> CommonResponseModel:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(file.filename)
            blob.upload_from_file(file.file)
            return CommonResponseModel(
                status="success",
                message="Image uploaded successfully",
                data={
                    "image_url": blob.public_url,
                },
            )
        except (FirebaseError, UnknownError, InternalError) as firebase_error:
            logger.error(
                f"Error while uploading image: {firebase_error}",
            )
            raise firebase_error
