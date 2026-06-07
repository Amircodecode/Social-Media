from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.infrastructures.db.models.user import UserTable
from src.infrastructures.db.models.article import ArticleTable
from src.domain.entities.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User):
        model = UserTable(**user.model_dump())
        self.session.add(model)
        await self.session.commit()
        return User.model_validate(model)

    async def find_by_email(self, email):
        result = await self.session.execute(
            select(UserTable).where(UserTable.email == email)
        )
        model = result.scalar_one_or_none()
        return User.model_validate(model) if model else None

    async def find_by_id(self, id):
        result = await self.session.execute(select(UserTable).where(UserTable.id == id))
        model = result.scalar_one_or_none()
        return User.model_validate(model) if model else None

    async def delete(self, user_id):
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

    async def update(self, user: User):
        result = await self.session.execute(
            select(UserTable).where(UserTable.id == user.id)
        )
        model = result.scalar_one_or_none()
        if model:
            model.email = user.email
            model.full_name = user.full_name
            model.password = user.password
            model.is_verified = user.is_verified
            await self.session.commit()
        return User.model_validate(model)

    async def find_all(self):
        result = await self.session.execute(select(UserTable))
        models = result.scalars().all()
        return [User.model_validate(model) for model in models]

    async def find_by_verification_token(self, token):
        result = await self.session.execute(
            select(UserTable).where(UserTable.verification_token == token)
        )
        model = result.scalar_one_or_none()
        return User.model_validate(model) if model else None
