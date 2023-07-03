from typing import Optional

from beanie import PydanticObjectId
from pydantic import AnyUrl, BaseModel, root_validator


class CreateNoteModel(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    labels: Optional[list[str]] = None
    images: Optional[list[AnyUrl]] = None
    background_color_index: Optional[int] = None
    background_image_index: Optional[int] = None

    @root_validator(pre=True)
    def validate_title_notes(cls, values):  # noqa: N805
        title, notes = values.get("title"), values.get("notes")
        if not title and not notes:
            raise ValueError("Either title or notes must be present")
        return values


class UpdateNoteModel(CreateNoteModel):
    note_id: PydanticObjectId


class DeleteLabelFromNoteModel(BaseModel):
    note_id: PydanticObjectId
    label: str
