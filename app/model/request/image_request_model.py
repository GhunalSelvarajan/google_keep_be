from pydantic import AnyUrl, BaseModel


class UpdateImageRequestModel(BaseModel):
    image_urls: list[AnyUrl]
