from app.api.routes.authentication import router as authentication_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(authentication_router, prefix="/users", tags=["authentication"])
