from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models.like import LikeTable


class LikeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, **kwargs) -> LikeTable:
        model = LikeTable(**kwargs)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_article_id(self, article_id) -> list[LikeTable]:
        result = await self.session.execute(
            select(LikeTable).where(LikeTable.article_id == article_id)
        )
        return list(result.scalars().all())

    async def delete(self, id):
        result = await self.session.execute(select(LikeTable).where(LikeTable.id == id))
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
