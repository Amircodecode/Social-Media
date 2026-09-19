import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.create_article import CreateArticle
from src.application.use_cases.get_all_articles import GetAllArticles
from src.application.use_cases.get_article_by_id import GetArcticleById
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


@router.post("/", response_model=ArticleResponse, status_code=201)
async def create_post(
    data: CreateArticleRequest,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    article_repository = ArticleRepository(session)
    use_case = CreateArticle(article_repository)
    return await use_case.execute(
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
    session: AsyncSession = Depends(get_session),
):
    user_repository = UserRepository(session)
    article_repository = ArticleRepository(session)
    like_repository = LikeRepository(session)
    use_case = GetAllArticles(user_repository, article_repository, like_repository)
    return await use_case.execute(
        page=page, limit=limit, search=search, date_from=date_from, date_to=date_to
    )


@router.get("/{id}", response_model=ArticleResponse)
async def get_post(id: uuid.UUID, session: AsyncSession = Depends(get_session)):
    article_repository = ArticleRepository(session)
    use_case = GetArcticleById(article_repository)
    article = await use_case.execute(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.delete("/delete/{id}")
async def delete_post(
    id: uuid.UUID,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    article_repository = ArticleRepository(session)
    article = await article_repository.find_by_id(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this post"
        )
    await article_repository.delete(id)
    return {"message": "Post deleted successfully!!"}


@router.put("/update/{id}", response_model=ArticleResponse)
async def update_post(
    id: uuid.UUID,
    data: UpdateArticleRequest,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    article_repository = ArticleRepository(session)
    article = await article_repository.find_by_id(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to update this post"
        )

    updated_article = await article_repository.update(
        id, title=data.title, content=data.content
    )
    return updated_article
