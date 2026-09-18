import asyncio
from src.infrastructures.celery.celery_app import celery_app
from src.application.use_cases.cleanup import (
    delete_unverified_users,
    delete_old_articles,
)


@celery_app.task(name="src.infrastructures.celery.tasks.delete_unverified_users_task")
def delete_unverified_users_task():
    asyncio.run(delete_unverified_users())


@celery_app.task(name="src.infrastructures.celery.tasks.delete_old_articles_task")
def delete_old_articles_task():
    asyncio.run(delete_old_articles())
