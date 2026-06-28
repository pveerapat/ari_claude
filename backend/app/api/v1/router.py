from fastapi import APIRouter
from app.api.v1 import (
    auth,
    farms,
    files,
    follow_ups,
    health,
    notebook_entries,
    note_items,
    notifications,
    sync,
    trees,
    upload_queue,
    zones,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(farms.router)
api_router.include_router(zones.router)
api_router.include_router(trees.router)
api_router.include_router(notebook_entries.router)
api_router.include_router(note_items.router)
api_router.include_router(follow_ups.router)
api_router.include_router(notifications.router)
api_router.include_router(files.router)
api_router.include_router(upload_queue.router)
api_router.include_router(sync.router)
