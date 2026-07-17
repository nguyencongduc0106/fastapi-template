from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

master_router = APIRouter()

master_router.include_router(auth_router)
master_router.include_router(users_router)
