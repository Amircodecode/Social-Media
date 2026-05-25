from src.infrastructures.db.database import SessionLocal
from src.infrastructures.db.models.like import LikeTable
from src.infrastructures.mappers.like import to_model, to_entity
from sqlalchemy import select


class LikeRepository:
    async def save(self, like):
        async with SessionLocal() as session:
            model = to_model(like)
            session.add(model)
            await session.commit()
            return to_entity(model)

    async def find_by_article_id(self, id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(LikeTable).where(LikeTable.article_id == id)
            )
            models = result.scalars().all()
            return [to_entity(model) for model in models]

    async def delete(self, id):
        async with SessionLocal() as session:
            result = await session.execute(select(LikeTable).where(LikeTable.id == id))
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
