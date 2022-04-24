from app.api.routes.users import router as users_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
