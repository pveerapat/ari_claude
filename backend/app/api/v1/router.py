from fastapi import APIRouter
from app.api.v1 import auth, farms, health, trees, zones

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(farms.router)
api_router.include_router(zones.router)
api_router.include_router(trees.router)
