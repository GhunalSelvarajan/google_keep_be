from beanie import PydanticObjectId
from pydantic import BaseModel


class UpdateLabelRequestModel(BaseModel):
    label_id: PydanticObjectId
    label_name: str
