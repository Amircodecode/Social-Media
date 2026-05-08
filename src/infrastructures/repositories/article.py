from ..db.database import SessionLocal
from ..db.models.article import ArticleTable
from ..mappers.article import to_model, to_entity
from sqlalchemy import select
from sqlalchemy import delete as sql_delete
from src.infrastructures.db.models import LikeTable
from src.infrastructures.db.models import CommentTable


class ArticleRepository:
    async def save(self, article):
        async with SessionLocal() as session:
            model = to_model(article)
            session.add(model)
            await session.commit()
            return to_entity(model)

    async def find_by_id(self, id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(ArticleTable).where(ArticleTable.id == id)
            )
            model = result.scalar_one_or_none()
            if model:
                return to_entity(model)
            return None

    async def delete(self, id):
        async with SessionLocal() as session:
            await session.execute(
                sql_delete(LikeTable).where(LikeTable.article_id == id)
            )
            await session.execute(
                sql_delete(CommentTable).where(CommentTable.article_id == id)
            )
            result = await session.execute(
                select(ArticleTable).where(ArticleTable.id == id)
            )
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()

    async def find_all(self):
        async with SessionLocal() as session:
            result = await session.execute(select(ArticleTable))
            models = result.scalars().all()
            return [to_entity(model) for model in models]

    async def update(self, id, article):
        async with SessionLocal() as session:
            result = await session.execute(
                select(ArticleTable).where(ArticleTable.id == id)
            )
            model = result.scalar_one_or_none()
            if model:
                model.title = article.title
                model.content = article.content
                await session.commit()
                return to_entity(model)
            return None

    async def find_by_user_id(self, user_id):
        async with SessionLocal() as session:
            result = await session.execute(
                select(ArticleTable).where(ArticleTable.user_id == user_id)
            )
            models = result.scalars().all()
            return [to_entity(model) for model in models]
