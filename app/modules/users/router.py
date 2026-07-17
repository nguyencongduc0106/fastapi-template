from fastapi import APIRouter, Depends

from app.core.dependency import get_current_user

router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@router.get("/me")
async def get_me() -> None:
    return
