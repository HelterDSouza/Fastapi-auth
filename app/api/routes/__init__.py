from app.api.routes.authentication import router as authentication_router
from app.api.routes.users import router as users_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(authentication_router, prefix="/users", tags=["authentication"])
router.include_router(users_router, prefix="/user", tags=["users"])
