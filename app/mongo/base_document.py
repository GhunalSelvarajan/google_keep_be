from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    created_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())
