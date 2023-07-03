from beanie import PydanticObjectId
from beanie.exceptions import CollectionWasNotInitialized, DocumentWasNotSaved

from app.database import NotesDatabase
from app.model import (
    CommonResponseModel,
    CreateNoteModel,
    DeleteLabelFromNoteModel,
    UpdateNoteModel,
)
from app.mongo import NoteDocument
from app.utils import logger


class NotesController:
    @staticmethod
    async def create(request: CreateNoteModel) -> CommonResponseModel:
        """
        Create a new note
        """
        try:
            await NotesDatabase.create(request)
            response = CommonResponseModel(
                status="success",
                message="Note created successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while creating note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def update(request: UpdateNoteModel) -> CommonResponseModel:
        """
        Update an existing note
        """
        try:
            await NotesDatabase.update(request)
            response = CommonResponseModel(
                status="success",
                message="Note updated successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while updating note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete(note_id: PydanticObjectId, is_permanent: bool) -> CommonResponseModel:
        """
        Delete a note
        """
        try:
            await NotesDatabase.delete(note_id, is_permanent)
            response = CommonResponseModel(
                status="success",
                message="Note deleted successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while deleting note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def get_all_notes(get_trash: bool, get_pinned: bool, get_archived: bool) -> CommonResponseModel:
        """
        Get all notes based on active status
        """
        try:
            notes: list[NoteDocument] = await NotesDatabase.get_all_notes(get_trash, get_pinned, get_archived)
            response = CommonResponseModel(
                status="success",
                message="Notes fetched successfully",
                data=notes,
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while fetching notes: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def delete_label_from_note(request: DeleteLabelFromNoteModel) -> CommonResponseModel:
        """
        Delete label from an existing note
        """
        try:
            await NotesDatabase.delete_label_from_note(request)
            response = CommonResponseModel(
                status="success",
                message="Label removed successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while removing label from note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def pin_note(note_id: PydanticObjectId, unpin: bool) -> CommonResponseModel:
        """
        Pin a note
        """
        try:
            await NotesDatabase.pin_note(note_id=note_id, unpin=unpin)
            response = CommonResponseModel(
                status="success",
                message="Note pinned successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while pinning note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def archive_note(note_id: PydanticObjectId, un_archive: bool) -> CommonResponseModel:
        """
        Archive a note
        """
        try:
            await NotesDatabase.archive_note(
                note_id=note_id,
                un_archive=un_archive,
            )
            response = CommonResponseModel(
                status="success",
                message="Note archived successfully",
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while archiving note: {beanie_exception}")
            raise beanie_exception

    @staticmethod
    async def search_note(search_text: str) -> CommonResponseModel:
        """
        Search notes
        """
        try:
            notes: list[NoteDocument] = await NotesDatabase.search_notes(
                search_text=search_text,
            )
            response = CommonResponseModel(
                status="success",
                message="Note searched and retried successfully",
                data=notes,
            )
            return response
        except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
            logger.error(f"Error while archiving note: {beanie_exception}")
            raise beanie_exception
