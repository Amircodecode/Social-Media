from datetime import datetime
from sqlalchemy import delete
from src.infrastructures.db.database import SessionLocal
from src.infrastructures.db.models.user import UserTable
from src.infrastructures.db.models.article import ArticleTable


async def delete_unverified_users():
    async with SessionLocal() as session:
        await session.execute(
            delete(UserTable).where(
                ~UserTable.is_verified,
                UserTable.token_expires_at < datetime.now(),
            )
        )
        await session.commit()


async def delete_old_articles():
    async with SessionLocal() as session:
        await session.execute(delete(ArticleTable))
        await session.commit()
