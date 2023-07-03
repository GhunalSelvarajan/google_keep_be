from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.mongo.base_document import BaseDocument
from app.mongo.notes_document import LabelDocument, NoteDocument


async def init_mongo(settings):
    client = AsyncIOMotorClient(settings.MONGO_HOST)
    await init_beanie(
        database=client.GoogleKeepClone,
        document_models=[
            BaseDocument,
            NoteDocument,
            LabelDocument,
        ],
    )


__all__ = [
    "init_mongo",
    "BaseDocument",
    "NoteDocument",
    "LabelDocument",
]
