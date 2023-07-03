from datetime import datetime
from typing import Optional

import pymongo
from beanie import Delete, Indexed, Insert, PydanticObjectId, Update, before_event
from box import Box
from pydantic import AnyUrl, Field

from app.mongo import BaseDocument
from app.utils import logger


class LabelDocument(BaseDocument):
    label: Indexed(str, unique=True)

    class Settings:
        name = "Labels"
        use_state_management = True
        state_management_save_previous = True

    @staticmethod
    @before_event(Update)
    async def update_notes(event: Update):
        event.updated_at = datetime.utcnow()
        previous_state: Box = Box(event.get_saved_state())
        try:
            collection = NoteDocument.get_motor_collection()

            cursor = collection.find({"labels": previous_state.label}, {"_id": 1})
            ids = [doc["_id"] for doc in await cursor.to_list(length=None)]

            await collection.update_many({"_id": {"$in": ids}}, {"$pull": {"labels": previous_state.label}})

            await collection.update_many({"_id": {"$in": ids}}, {"$addToSet": {"labels": event.label}})
        except Exception as exception:
            logger.error(f"Cannot update notes: {exception}")

    @before_event(Delete)
    async def remove_from_notes(self):
        await NoteDocument.get_motor_collection().update_many(
            {"label_ids": self.id}, {"$pull": {"label_ids": self.id, "labels": self.label}}
        )


class NoteDocument(BaseDocument):
    title: Optional[str] = None
    notes: Optional[str] = None
    label_ids: Optional[list[PydanticObjectId]] = Field(default_factory=list)
    labels: Optional[list[str]] = Field(default_factory=list)
    images: Optional[list[AnyUrl]] = None
    background_color_index: Optional[str] = None
    background_image_index: Optional[str] = None
    active: bool = True
    pinned: bool = False
    archived: bool = False
    order: int = 0

    class Settings:
        name = "Notes"
        indexes = [
            [
                ("title", pymongo.TEXT),
                ("notes", pymongo.TEXT),
                ("labels", pymongo.TEXT),
            ],
            [
                ("order", pymongo.ASCENDING),
            ],
        ]

    @before_event(Insert)
    async def set_label_ids(self):
        if len(self.labels) > 0:
            for label in self.labels:
                label_document = await LabelDocument.find_one({"label": label})
                if label_document is None:
                    label_document = await LabelDocument(label=label).insert()
                self.label_ids.append(label_document.id)

    @before_event(Update)
    async def set_updated_at(self):
        self.updated_at = datetime.utcnow()

    @before_event(Insert)
    async def set_order(self):
        max_order_number = await NoteDocument.find_all().sort(("order", pymongo.DESCENDING)).to_list(1)
        if max_order_number:
            self.order = max_order_number[0].order + 1
        else:
            self.order = 1
