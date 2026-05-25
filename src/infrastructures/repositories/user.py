from src.infrastructures.db.database import SessionLocal
from src.infrastructures.db.models.user import UserTable
from src.infrastructures.mappers.user import to_model, to_entity
from src.domain.entities.user import User
from sqlalchemy import select
from sqlalchemy import delete
from src.infrastructures.db.models.article import ArticleTable


class UserRepository:
    async def save(self, user: User):
        async with SessionLocal() as session:
            model = to_model(user)
            session.add(model)
            await session.commit()
            return to_entity(model)

    async def find_by_email(self, email):
        async with SessionLocal() as session:
            result = await session.execute(
                select(UserTable).where(UserTable.email == email)
            )
            model = result.scalar_one_or_none()
            if model:
                return to_entity(model)
            return None

    async def find_by_id(self, id):
        async with SessionLocal() as session:
            result = await session.execute(select(UserTable).where(UserTable.id == id))
            model = result.scalar_one_or_none()
            if model:
                return to_entity(model)
            return None

    async def delete(self, user_id):
        async with SessionLocal() as session:
            await session.execute(
                delete(ArticleTable).where(ArticleTable.user_id == user_id)
            )
            result = await session.execute(
                select(UserTable).where(UserTable.id == user_id)
            )
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()

    async def update(self, user):
        async with SessionLocal() as session:
            result = await session.execute(
                select(UserTable).where(UserTable.id == user.id)
            )
            model = result.scalar_one_or_none()
            if model:
                model.email = user.email
                model.full_name = user.full_name
                model.password = user.password
                model.is_verified = user.is_verified
                await session.commit()
                return to_entity(model)

    async def find_all(self):
        async with SessionLocal() as session:
            result = await session.execute(select(UserTable))
            models = result.scalars().all()
            return [to_entity(model) for model in models]

    async def find_by_verification_token(self, token):
        async with SessionLocal() as session:
            result = await session.execute(
                select(UserTable).where(UserTable.verification_token == token)
            )
            model = result.scalar_one_or_none()
            if model:
                return to_entity(model)
