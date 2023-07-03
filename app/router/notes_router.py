from beanie import PydanticObjectId
from beanie.exceptions import CollectionWasNotInitialized, DocumentWasNotSaved
from fastapi import APIRouter

from app.constants import DEFAULT_ROUTER_SETTINGS
from app.controller import NotesController
from app.model import (
    CommonResponseModel,
    CreateNoteModel,
    DeleteLabelFromNoteModel,
    UpdateNoteModel,
)

notes_router = APIRouter(
    tags=["Notes"],
)


@notes_router.post(
    "",
    name="Create note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def create(request: CreateNoteModel) -> CommonResponseModel:
    """
    Create a new note
    """
    try:
        response: CommonResponseModel = await NotesController.create(request)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while creating note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.put(
    "",
    name="Update note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def update(request: UpdateNoteModel) -> CommonResponseModel:
    """
    Update an existing note
    """
    try:
        response: CommonResponseModel = await NotesController.update(request)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while updating note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.delete(
    "",
    name="Delete note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def delete(note_id: PydanticObjectId, is_permanent: bool = False) -> CommonResponseModel:
    """
    Delete a note
    """
    try:
        response: CommonResponseModel = await NotesController.delete(note_id, is_permanent)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while deleting note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.delete(
    "/label",
    name="Remove label from Note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def remove_label(request: DeleteLabelFromNoteModel) -> CommonResponseModel:
    """
    Delete label from an existing note
    """
    try:
        response: CommonResponseModel = await NotesController.delete_label_from_note(request)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while removing label from note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.get(
    "/",
    name="Get all notes",
    **DEFAULT_ROUTER_SETTINGS,
)
async def get(
    get_trash: bool = False,
    get_pinned: bool = False,
    get_archived: bool = False,
) -> CommonResponseModel:
    """
    Get all notes based on active, trash and pinned status
    """
    try:
        response: CommonResponseModel = await NotesController.get_all_notes(
            get_trash,
            get_pinned,
            get_archived,
        )
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while fetching notes: {beanie_exception}",
            error=str(beanie_exception),
        )
    except ValueError as value_error:
        return CommonResponseModel(
            status="failure",
            message="Get pinned and get trash cannot be true at the same time",
            error=str(value_error),
        )


@notes_router.put(
    "/pin",
    name="Pin note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def pin_note(note_id: PydanticObjectId, unpin: bool = False) -> CommonResponseModel:
    """
    Pin or Unpin a note
    """
    try:
        response: CommonResponseModel = await NotesController.pin_note(note_id, unpin)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while pinning note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.put(
    "/archive",
    name="Archive note",
    **DEFAULT_ROUTER_SETTINGS,
)
async def archive_note(note_id: PydanticObjectId, un_archive: bool = False) -> CommonResponseModel:
    """
    Archive or Un Archive a note
    """
    try:
        response: CommonResponseModel = await NotesController.archive_note(note_id, un_archive)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while archiving note: {beanie_exception}",
            error=str(beanie_exception),
        )


@notes_router.get(
    "/search",
    name="Search notes",
    **DEFAULT_ROUTER_SETTINGS,
)
async def search_note(search_text: str) -> CommonResponseModel:
    """
    Search notes based on title, label and note
    """
    try:
        response: CommonResponseModel = await NotesController.search_note(search_text)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while searching note: {beanie_exception}",
            error=str(beanie_exception),
        )
