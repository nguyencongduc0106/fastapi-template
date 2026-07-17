from collections.abc import AsyncGenerator
from typing import Annotated, Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import SessionLocal
from app.core.exception import UnauthorizedError
from app.core.security import bearer_scheme, decode_access_token


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> dict[str, Any]:
    if not credentials:
        raise UnauthorizedError()
    try:
        payload = decode_access_token(credentials.credentials)
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError(detail="Token has expired") from None
    except jwt.PyJWTError:
        raise UnauthorizedError() from None
