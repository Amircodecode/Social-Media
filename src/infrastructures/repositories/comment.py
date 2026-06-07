from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models.comment import CommentTable
from src.domain.entities.comment import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, comment: Comment):
        model = CommentTable(**comment.model_dump())
        self.session.add(model)
        await self.session.commit()
        return Comment.model_validate(model)

    async def find_by_article_id(self, article_id):
        result = await self.session.execute(
            select(CommentTable).where(CommentTable.article_id == article_id)
        )
        models = result.scalars().all()
        return [Comment.model_validate(model) for model in models]

    async def delete(self, id):
        result = await self.session.execute(
            select(CommentTable).where(CommentTable.id == id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
