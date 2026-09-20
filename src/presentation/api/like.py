import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructures.auth.dependencies import get_current_user
from src.application.services.like_service import LikeService
from src.application.dtos.like import CreateLikeRequest
from src.infrastructures.repositories.like import LikeRepository
from src.infrastructures.repositories.article import ArticleRepository
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable

router = APIRouter(prefix="/likes", tags=["likes"])


def get_like_service(session: AsyncSession = Depends(get_session)) -> LikeService:
    return LikeService(LikeRepository(session), ArticleRepository(session))


@router.post("/", status_code=201)
async def create_like(
    data: CreateLikeRequest,
    current_user: UserTable = Depends(get_current_user),
    service: LikeService = Depends(get_like_service),
):
    return await service.create(
        article_id=data.article_id,
        user_id=current_user.id,
        is_verified=current_user.is_verified,
    )


@router.delete("/delete/{id}")
async def delete_like(
    id: uuid.UUID,
    current_user: UserTable = Depends(get_current_user),
    service: LikeService = Depends(get_like_service),
):
    await service.delete(id, current_user.id)
    return {"message": "Like deleted successfully!!"}
