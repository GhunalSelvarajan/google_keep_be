from beanie import PydanticObjectId
from beanie.exceptions import CollectionWasNotInitialized, DocumentWasNotSaved

from app.model import UpdateLabelRequestModel
from app.mongo import LabelDocument, NoteDocument
from app.utils import logger


class LabelDatabase:
    @staticmethod
    async def get_all_labels() -> list[LabelDocument]:
        try:
            labels = await LabelDocument.find_all().to_list()
            return labels
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error("Error while getting all labels: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def get_all_notes_by_label_id(label_id: PydanticObjectId) -> list[NoteDocument]:
        try:
            notes = await NoteDocument.find({"label_ids": label_id}).to_list()
            return notes
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error("Error while getting all labels: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def update(request: UpdateLabelRequestModel) -> None:
        try:
            label = await LabelDocument.find_one({"_id": request.label_id})
            if label:
                label.label = request.label_name
                await label.save()
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while updating label: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete(label_id: PydanticObjectId) -> None:
        try:
            label = await LabelDocument.find_one({"_id": label_id})
            if label:
                await label.delete()
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while deleting label: {beanie_exception}")
            raise beanie_exception
