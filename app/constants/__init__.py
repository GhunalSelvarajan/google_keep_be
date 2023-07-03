from app.constants.app_literals import STATUS_TYPE_LITERAL
from app.model import CommonResponseModel

BASE_SLUG = "/api/v1"

DEFAULT_ROUTER_SETTINGS = {
    "response_model_exclude_none": True,
    "response_model": CommonResponseModel,
}

__all__ = [
    "BASE_SLUG",
    "STATUS_TYPE_LITERAL",
    "DEFAULT_ROUTER_SETTINGS",
]
