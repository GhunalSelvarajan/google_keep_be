from box import Box

from app.constants import BASE_SLUG
from app.router import image_router, labels_router, notes_router

ROUTER_CONFIGS: Box = Box(
    {
        "configs": [
            {
                "prefix": f"{BASE_SLUG}/notes",
                "router": notes_router,
            },
            {
                "prefix": f"{BASE_SLUG}/labels",
                "router": labels_router,
            },
            {
                "prefix": f"{BASE_SLUG}/image",
                "router": image_router,
            },
        ]
    }
)
