from datetime import UTC, datetime
from typing import NoReturn
from uuid import UUID

import jwt
from redis.asyncio import Redis

from app.core.config import app_settings
from app.core.exception import ConflictError, UnauthorizedError
from app.core.redis import redis_keys
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_jwt_token,
    hash_password,
    verify_password,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schema import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    TokenResponse,
)
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schema import UserCreate


class AuthService:
    def __init__(self, repo: AuthRepository, redis: Redis):
        self.repo = repo
        self.redis = redis
        self.user_repo = UserRepository(repo.db)

    def _refresh_key(self, token: str) -> str:
        return redis_keys.refresh_token(token)

    async def _store_refresh_token(self, refresh_token: str, user_id: UUID) -> None:
        await self.redis.set(
            self._refresh_key(refresh_token),
            str(user_id),
            ex=app_settings.JWT_REFRESH_EXPIRE_DAYS * 24 * 60 * 60,
        )

    async def _issue_tokens(self, user: User) -> TokenResponse:
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        await self._store_refresh_token(refresh_token, user.id)
        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    async def _revoke_refresh_token(self, refresh_token: str) -> None:
        await self.redis.delete(self._refresh_key(refresh_token))

    def _invalid_refresh(self, exc: Exception | None = None) -> NoReturn:
        err = UnauthorizedError("Invalid refresh token")
        if exc is not None:
            raise err from exc
        raise err

    async def register(self, body: UserCreate) -> User:
        if await self.user_repo.get_by_email(body.email):
            raise ConflictError("User with this email already exists")
        data = body.model_dump(exclude={"password"})
        data["password_hash"] = hash_password(body.password)
        return await self.user_repo.create(**data)

    async def login(self, body: LoginRequest) -> TokenResponse:
        user = await self.user_repo.get_by_email(body.email)
        if not user or not verify_password(body.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        return await self._issue_tokens(user)

    async def refresh(self, body: RefreshRequest) -> TokenResponse:
        token = body.refresh_token
        try:
            payload = decode_jwt_token(token)
        except jwt.PyJWTError as exc:
            await self._revoke_refresh_token(token)
            self._invalid_refresh(exc)
        user_id_raw = payload.get("sub")
        if payload.get("type") != "refresh" or not user_id_raw:
            await self._revoke_refresh_token(token)
            self._invalid_refresh()
        try:
            user_id = UUID(user_id_raw)
        except ValueError as exc:
            await self._revoke_refresh_token(token)
            self._invalid_refresh(exc)
        if not await self.redis.exists(self._refresh_key(token)):
            self._invalid_refresh()
        user = await self.user_repo.get(user_id)
        if not user:
            await self._revoke_refresh_token(token)
            self._invalid_refresh()
        await self._revoke_refresh_token(token)
        return await self._issue_tokens(user)

    async def logout(self, body: LogoutRequest) -> None:
        await self._revoke_refresh_token(body.refresh_token)

        if body.access_token:
            try:
                payload = decode_jwt_token(body.access_token)
                if payload.get("type") != "access":
                    return
                jti = payload.get("jti")
                exp = payload.get("exp")
                if not jti or exp is None:
                    return
                ttl = max(int(exp - datetime.now(UTC).timestamp()), 1)
                await self.redis.set(redis_keys.blacklist_jti(jti), "1", ex=ttl)
            except jwt.PyJWTError:
                pass

    async def verify(self, token: str) -> None:
        pass
        # decoded_token = decode_token(token)
        # user = await self.user_repo.get(decoded_token.id)
        # if not user:
        #     raise UnauthorizedError("Invalid token")
        # return await self.repo.verify(user)
