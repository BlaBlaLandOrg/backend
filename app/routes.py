from fastapi import APIRouter

from app.api.views import router as api

router = APIRouter()

router.include_router(api, prefix="/api", tags=["api"])
