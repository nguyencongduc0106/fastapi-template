from typing import Any
from uuid import UUID

from fastapi import APIRouter

from app.core.dependency import CurrentUserDep
from app.core.exception import UnauthorizedError
from app.modules.users.dependency import UserServiceDep
from app.modules.users.model import User
from app.modules.users.schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


def _user_id_from_token(current_user: dict[str, Any]) -> UUID:
    try:
        return UUID(current_user["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise UnauthorizedError(detail="Invalid token subject") from exc


@router.get("/me", response_model=UserResponse)
async def get_me(
    service: UserServiceDep,
    current_user: CurrentUserDep,
) -> User:
    return await service.get(_user_id_from_token(current_user))
