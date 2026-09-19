from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.infrastructures.db.models.comment import CommentTable


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> CommentTable:
        model = CommentTable(**kwargs)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_article_id(self, article_id) -> list[CommentTable]:
        result = await self.session.execute(
            select(CommentTable).where(CommentTable.article_id == article_id)
        )
        return list(result.scalars().all())

    async def delete(self, comment_id) -> None:
        result = await self.session.execute(
            select(CommentTable).where(CommentTable.id == comment_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
