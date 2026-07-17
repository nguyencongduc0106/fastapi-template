from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import jwt
from bcrypt import checkpw, gensalt, hashpw
from fastapi.security import HTTPBearer

from app.core.config import app_settings


def hash_password(password: str) -> str:
    return hashpw(password.encode(), gensalt()).decode()


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return checkpw(
        plain_password.encode(),
        hashed_password.encode(),
    )


def create_access_token(payload: dict[str, Any]) -> str:
    return jwt.encode(
        payload={
            **payload,
            "jti": str(uuid4()),
            "iat": datetime.now(UTC),
            "exp": datetime.now(UTC)
            + timedelta(minutes=app_settings.JWT_EXPIRE_MINUTES),
        },
        key=app_settings.JWT_SECRET,
        algorithm=app_settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        app_settings.JWT_SECRET,
        algorithms=[app_settings.JWT_ALGORITHM],
    )


bearer_scheme = HTTPBearer(
    auto_error=False,
)
