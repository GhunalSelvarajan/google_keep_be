from beanie import PydanticObjectId
from beanie.exceptions import CollectionWasNotInitialized, DocumentWasNotSaved
from fastapi import APIRouter

from app.constants import DEFAULT_ROUTER_SETTINGS
from app.controller import LabelController
from app.model import CommonResponseModel, UpdateLabelRequestModel

labels_router = APIRouter(
    tags=["Labels"],
)


@labels_router.get("", name="Get all labels", **DEFAULT_ROUTER_SETTINGS)
async def get() -> CommonResponseModel:
    """
    Get all labels
    """
    try:
        response: CommonResponseModel = await LabelController.get_all_labels()
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while fetching labels: {beanie_exception}",
            error=str(beanie_exception),
        )


@labels_router.get("/notes", name="Get all notes for each label", **DEFAULT_ROUTER_SETTINGS)
async def get_all_notes_by_label_id(label_id: PydanticObjectId) -> CommonResponseModel:
    """
    Get all notes for each label
    """
    try:
        response: CommonResponseModel = await LabelController.get_all_notes_by_label_id(label_id)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while fetching labels: {beanie_exception}",
            error=str(beanie_exception),
        )


@labels_router.put("", name="Edit an existing label", **DEFAULT_ROUTER_SETTINGS)
async def update(request: UpdateLabelRequestModel) -> CommonResponseModel:
    """
    Edit an existing labels
    """
    try:
        response: CommonResponseModel = await LabelController.update(request)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while updating label: {beanie_exception}",
            error=str(beanie_exception),
        )


@labels_router.delete("", name="Delete an existing label", **DEFAULT_ROUTER_SETTINGS)
async def delete(label_id: PydanticObjectId) -> CommonResponseModel:
    """
    Delete an existing labels
    """
    try:
        response: CommonResponseModel = await LabelController.delete(label_id)
        return response
    except (DocumentWasNotSaved, CollectionWasNotInitialized) as beanie_exception:
        return CommonResponseModel(
            status="failure",
            message=f"Error while deleting label: {beanie_exception}",
            error=str(beanie_exception),
        )
