from src.infrastructures.db.database import SessionLocal
from src.infrastructures.db.models.comment import CommentTable
from src.infrastructures.mappers.comment import to_model, to_entity
from sqlalchemy import select


class CommentRepository:
    async def save(self, comment):
        async with SessionLocal() as session:
            model = to_model(comment)
            session.add(model)
            await session.commit()
            return to_entity(model)

    async def find_by_article_id(self, article_id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(CommentTable).where(CommentTable.article_id == article_id)
            )
            models = result.scalars().all()
            if models:
                return [to_entity(model) for model in models]
            return None

    async def delete(self, id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(CommentTable).where(CommentTable.id == id)
            )
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
