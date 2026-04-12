# Import all routers
from app.api.v1.routers.auth import router as auth_router
from app.api.v1.routers.incidents import router as incidents_router
from app.api.v1.routers.media import router as media_router
from app.api.v1.routers.resources import router as resources_router
from app.api.v1.routers.reports import router as reports_router
from app.api.v1.routers.websocket import router as websocket_router
from app.api.v1.routers.integrations import router as integrations_router
from app.api.v1.routers.debug import router as debug_router

__all__ = [
    "auth_router",
    "incidents_router",
    "media_router",
    "resources_router",
    "reports_router",
    "websocket_router",
    "integrations_router",
    "debug_router"
]
