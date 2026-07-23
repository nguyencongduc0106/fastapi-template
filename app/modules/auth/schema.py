from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LogoutRequest(BaseModel):
    refresh_token: str
    access_token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str
