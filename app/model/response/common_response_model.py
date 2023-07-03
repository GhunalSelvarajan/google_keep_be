from typing import Any, Optional

from pydantic import BaseModel

from app.constants.app_literals import STATUS_TYPE_LITERAL


class CommonResponseModel(BaseModel):
    status: STATUS_TYPE_LITERAL
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
