import pymongo
from beanie import PydanticObjectId
from beanie.exceptions import (
    CollectionWasNotInitialized,
    DocumentNotFound,
    DocumentWasNotSaved,
)

from app.model import CreateNoteModel, DeleteLabelFromNoteModel, UpdateNoteModel
from app.mongo import LabelDocument, NoteDocument
from app.utils import logger


class NotesDatabase:
    @staticmethod
    async def create(request: CreateNoteModel) -> None:
        """
        Create a new note
        """
        try:
            await NoteDocument(**request.dict()).create()
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while creating note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def update(request: UpdateNoteModel) -> None:
        """
        Updating an existing note
        """
        try:
            note_object = await NoteDocument.find_one({"_id": request.note_id})
            for label in request.labels:
                if label not in note_object.labels:
                    label_object = await LabelDocument(label=label).insert()
                    note_object.label_ids.append(label_object.id)
            for label in note_object.labels:
                if label not in request.labels:
                    label_object = await LabelDocument.find_one({"label": label})
                    if label_object:
                        note_object.label_ids.remove(label_object.id)

            note_object.title = request.title
            note_object.notes = request.notes
            note_object.labels = request.labels
            note_object.images = request.images
            note_object.background_color_index = request.background_color_index
            note_object.background_image_index = request.background_image_index
            await note_object.save()
        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while updating note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete(note_id: PydanticObjectId, is_permanent: bool) -> None:
        """
        Delete a note
        """
        try:
            note_object = await NoteDocument.find_one({"_id": note_id})
            if is_permanent and note_object:
                await note_object.delete()
            else:
                note_object.active = False
                await note_object.save()
        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while deleting a note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def get_all_notes(get_trash: bool, get_pinned: bool, get_archived: bool) -> list[NoteDocument]:
        """
        Get all notes based on active, trash and pinned status
        """
        try:
            if get_trash and get_pinned:
                raise ValueError("get_trash and get_pinned cannot be true at the same time")
            if get_trash:
                return (
                    await NoteDocument.find({"active": False})
                    .sort(
                        [
                            ("updated_at", pymongo.DESCENDING),
                        ]
                    )
                    .to_list()
                )
            if get_pinned:
                return (
                    await NoteDocument.find({"pinned": True})
                    .sort(
                        [
                            ("updated_at", pymongo.DESCENDING),
                        ]
                    )
                    .to_list()
                )
            if get_archived:
                return (
                    await NoteDocument.find({"archived": True})
                    .sort(
                        [
                            ("updated_at", pymongo.DESCENDING),
                        ]
                    )
                    .to_list()
                )
            else:
                return await NoteDocument.find(
                    {"active": True},
                    {"archived": False},
                ).to_list()
        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while getting notes: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete_label_from_note(request: DeleteLabelFromNoteModel) -> None:
        """
        Delete label from an existing note
        """
        try:
            note_object = await NoteDocument.find_one({"_id": request.note_id})
            if request.label in note_object.labels:
                note_object.labels.remove(request.label)
                label_object = await LabelDocument.find_one({"label": request.label})
                note_object.label_ids.remove(label_object.id)
                await note_object.save()
        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while deleting label from note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def pin_note(note_id: PydanticObjectId, unpin: bool) -> None:
        """
        Pin a note
        """
        try:
            note_object = await NoteDocument.find_one({"_id": note_id})
            if note_object.pinned and unpin:
                note_object.pinned = False
                await note_object.save()
            if not note_object.pinned and not unpin:
                note_object.pinned = True
                await note_object.save()
        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while pinning note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def archive_note(note_id: PydanticObjectId, un_archive: bool) -> None:
        """
        Archive a note
        """
        try:
            note_object = await NoteDocument.find_one({"_id": note_id})
            if note_object.archived and un_archive:
                note_object.archived = False
                await note_object.save()
            if not note_object.archived and not un_archive:
                note_object.archived = True
                await note_object.save()

        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while archiving note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def search_notes(search_text: str) -> list[NoteDocument]:
        """
        Search notes
        """
        try:
            notes = await NoteDocument.find({"$text": {"$search": search_text}, "active": True}).to_list()

            return notes

        except (DocumentWasNotSaved, CollectionWasNotInitialized, DocumentNotFound) as beanie_exception:
            logger.error(f"Error while archiving note: {beanie_exception}")
            raise beanie_exception
