import uuid
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.article_service import ArticleService
from src.application.dtos.article import (
    CreateArticleRequest,
    UpdateArticleRequest,
    ArticleResponse,
)
from src.infrastructures.repositories.article import ArticleRepository
from src.infrastructures.repositories.user import UserRepository
from src.infrastructures.repositories.like import LikeRepository
from src.infrastructures.auth.dependencies import get_current_user
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable

router = APIRouter(prefix="/posts", tags=["posts"])


def get_article_service(session: AsyncSession = Depends(get_session)) -> ArticleService:
    return ArticleService(
        ArticleRepository(session),
        LikeRepository(session),
        UserRepository(session),
    )


@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_post(
    data: CreateArticleRequest,
    current_user: UserTable = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    return await service.create(
        title=data.title,
        content=data.content,
        user_id=current_user.id,
        is_verified=current_user.is_verified,
    )


@router.get("/all")
async def get_all_posts(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    service: ArticleService = Depends(get_article_service),
):
    return await service.get_all(
        page=page, limit=limit, search=search, date_from=date_from, date_to=date_to
    )


@router.get("/{id}", response_model=ArticleResponse)
async def get_post(
    id: uuid.UUID, service: ArticleService = Depends(get_article_service)
):
    return await service.get_by_id(id)


@router.delete("/delete/{id}")
async def delete_post(
    id: uuid.UUID,
    current_user: UserTable = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    await service.delete(id, current_user.id)
    return {"message": "Post deleted successfully!!"}


@router.put("/update/{id}", response_model=ArticleResponse)
async def update_post(
    id: uuid.UUID,
    data: UpdateArticleRequest,
    current_user: UserTable = Depends(get_current_user),
    service: ArticleService = Depends(get_article_service),
):
    return await service.update(id, current_user.id, data.title, data.content)
