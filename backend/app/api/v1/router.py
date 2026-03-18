from fastapi import APIRouter

from app.api.v1.health.router import router as health_router
from app.api.v1.user.router import router as user_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
