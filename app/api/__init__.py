from fastapi import APIRouter
from app.routers.plane import router as plane_router

router = APIRouter()
router.include_router(plane_router)