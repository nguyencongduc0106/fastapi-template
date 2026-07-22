from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[ModelType]:
    def __init__(self, db: AsyncSession, model: type[ModelType]):
        self.db = db
        self.model = model

    async def create(self, **kwargs: Any) -> ModelType:
        obj = self.model(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def get(self, id: UUID) -> ModelType | None:
        return await self.db.get(self.model, id)

    async def get_all(self) -> list[ModelType]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def update(self, obj: ModelType, **kwargs: Any) -> ModelType:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.db.delete(obj)
        await self.db.flush()
