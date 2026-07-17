from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    APP_NAME: str = "FastAPI Template"
    APP_URL: str = "http://localhost:8000"

    CORS_ALLOW_ORIGINS: list[str] = Field(default_factory=list)

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: str = ""
    POSTGRES_DB: str = ""

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    REDIS_HOST: str = ""
    REDIS_PORT: str = ""

    def REDIS_URL(self, db: int) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"

    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = ""
    JWT_EXPIRE_MINUTES: int = 0

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )


app_settings = AppSettings()
