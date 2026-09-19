from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from src.infrastructures.db.models.article import ArticleTable
from src.infrastructures.db.models.like import LikeTable
from src.infrastructures.db.models.comment import CommentTable
from sqlalchemy.orm import joinedload


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> ArticleTable:
        model = ArticleTable(**kwargs)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_id(self, article_id) -> ArticleTable | None:
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.id == article_id)
        )
        return result.scalar_one_or_none()

    async def delete(self, article_id) -> None:
        await self.session.execute(
            sql_delete(LikeTable).where(LikeTable.article_id == article_id)
        )
        await self.session.execute(
            sql_delete(CommentTable).where(CommentTable.article_id == article_id)
        )
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.id == article_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()

    async def find_all(self) -> list[ArticleTable]:
        result = await self.session.execute(select(ArticleTable))
        return list(result.scalars().all())

    async def find_by_user_id(self, user_id) -> list[ArticleTable]:
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.user_id == user_id)
        )
        return list(result.scalars().all())

    async def update(self, article_id, **kwargs) -> ArticleTable | None:
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.id == article_id)
        )
        model = result.scalar_one_or_none()
        if model:
            for field, value in kwargs.items():
                setattr(model, field, value)
            await self.session.commit()
            await self.session.refresh(model)
        return model

    async def find_all_with_filters(
        self, search=None, date_from=None, date_to=None, limit=10, offset=0
    ):
        query = select(ArticleTable).options(joinedload(ArticleTable.user))

        if search:
            query = query.where(ArticleTable.title.ilike(f"%{search}%"))
        if date_from:
            query = query.where(ArticleTable.created_at >= date_from)
        if date_to:
            query = query.where(ArticleTable.created_at <= date_to)

        query = (
            query.order_by(ArticleTable.created_at.desc()).limit(limit).offset(offset)
        )

        result = await self.session.execute(query)
        return result.unique().scalars().all()
