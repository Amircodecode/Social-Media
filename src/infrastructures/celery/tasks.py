import asyncio
from src.infrastructures.celery.celery_app import celery_app
from src.application.services.cleanup_service import CleanupService

cleanup_service = CleanupService()


@celery_app.task
def delete_unverified_users_task():
    asyncio.run(cleanup_service.delete_unverified_users())


@celery_app.task
def delete_old_articles_task():
    asyncio.run(cleanup_service.delete_old_articles())
