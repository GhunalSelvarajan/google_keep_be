from beanie import PydanticObjectId
from beanie.exceptions import CollectionWasNotInitialized, DocumentWasNotSaved

from app.database import LabelDatabase
from app.model import CommonResponseModel, UpdateLabelRequestModel
from app.utils import logger


class LabelController:
    @staticmethod
    async def get_all_labels() -> CommonResponseModel:
        """
        Get all labels
        """
        try:
            labels = await LabelDatabase.get_all_labels()
            return CommonResponseModel(
                status="success",
                message="Labels fetched successfully",
                data=labels,
            )
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while getting labels: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def get_all_notes_by_label_id(label_id: PydanticObjectId) -> CommonResponseModel:
        """
        Get all notes for each label
        """
        try:
            notes = await LabelDatabase.get_all_notes_by_label_id(label_id)
            return CommonResponseModel(
                status="success",
                message="Notes fetched successfully",
                data=notes,
            )
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while fetching notes for label: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def update(request: UpdateLabelRequestModel) -> CommonResponseModel:
        """
        Edit an existing labels
        """
        try:
            labels = await LabelDatabase.update(request)
            return CommonResponseModel(
                status="success",
                message="Label updated successfully",
                data=labels,
            )
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while updating label: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete(label_id: PydanticObjectId) -> CommonResponseModel:
        """
        Edit an existing labels
        """
        try:
            labels = await LabelDatabase.delete(label_id)
            return CommonResponseModel(
                status="success",
                message="Label deleted successfully",
                data=labels,
            )
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while deleting label: {beanie_exception}")
            raise beanie_exception
