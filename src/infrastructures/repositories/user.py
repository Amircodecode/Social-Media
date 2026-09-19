from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.infrastructures.db.models.user import UserTable
from src.infrastructures.db.models.article import ArticleTable


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> UserTable:
        model = UserTable(**kwargs)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def find_by_email(self, email: str) -> UserTable | None:
        result = await self.session.execute(
            select(UserTable).where(UserTable.email == email)
        )
        return result.scalar_one_or_none()

    async def delete(self, user_id) -> None:
        await self.session.execute(
            delete(ArticleTable).where(ArticleTable.user_id == user_id)
        )
        result = await self.session.execute(
            select(UserTable).where(UserTable.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()

    async def update(self, user_id, **kwargs) -> UserTable | None:
        result = await self.session.execute(
            select(UserTable).where(UserTable.id == user_id)
        )
        model = result.scalar_one_or_none()
        if model:
            for field, value in kwargs.items():
                setattr(model, field, value)
            await self.session.commit()
            await self.session.refresh(model)
        return model

    async def find_all(self) -> list[UserTable]:
        result = await self.session.execute(select(UserTable))
        return list(result.scalars().all())

    async def find_by_verification_token(self, token) -> UserTable | None:
        result = await self.session.execute(
            select(UserTable).where(UserTable.verification_token == token)
        )
        return result.scalar_one_or_none()
