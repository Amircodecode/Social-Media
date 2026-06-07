from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from src.infrastructures.db.models.article import ArticleTable
from src.infrastructures.db.models.like import LikeTable
from src.infrastructures.db.models.comment import CommentTable
from src.domain.entities.article import Article
from src.domain.entities.user import User
from src.infrastructures.db.models.user import UserTable


class ArticleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, article: Article):
        model = ArticleTable(**article.model_dump())
        self.session.add(model)
        await self.session.commit()
        return Article.model_validate(model)

    async def find_by_id(self, id):
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.id == id)
        )
        model = result.scalar_one_or_none()
        return Article.model_validate(model) if model else None

    async def delete(self, id):
        await self.session.execute(
            sql_delete(LikeTable).where(LikeTable.article_id == id)
        )
        await self.session.execute(
            sql_delete(CommentTable).where(CommentTable.article_id == id)
        )
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.id == id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()

    async def find_all(self):
        result = await self.session.execute(select(ArticleTable))
        models = result.scalars().all()
        return [Article.model_validate(model) for model in models]

    async def update(self, user: User):
        result = await self.session.execute(
            select(UserTable).where(UserTable.id == user.id)
        )
        model = result.scalar_one_or_none()
        model.email = user.email
        model.full_name = user.full_name
        model.password = user.password
        model.is_verified = user.is_verified
        await self.session.commit()
        return User.model_validate(model)

    async def find_by_user_id(self, user_id):
        result = await self.session.execute(
            select(ArticleTable).where(ArticleTable.user_id == user_id)
        )
        models = result.scalars().all()
        return [Article.model_validate(model) for model in models]
