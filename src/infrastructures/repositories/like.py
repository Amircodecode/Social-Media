from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models.like import LikeTable
from src.domain.entities.like import Like


class LikeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, like: Like):
        model = LikeTable(**like.model_dump())
        self.session.add(model)
        await self.session.commit()
        return Like.model_validate(model)

    async def find_by_article_id(self, id):
        result = await self.session.execute(
            select(LikeTable).where(LikeTable.article_id == id)
        )
        models = result.scalars().all()
        return [Like.model_validate(model) for model in models]

    async def delete(self, id):
        result = await self.session.execute(select(LikeTable).where(LikeTable.id == id))
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
