import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructures.auth.dependencies import get_current_user
from src.application.services.comment_service import CommentService
from src.application.dtos.comment import CreateCommentRequest
from src.infrastructures.repositories.comment import CommentRepository
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable

router = APIRouter(prefix="/comments", tags=["comments"])


def get_comment_service(session: AsyncSession = Depends(get_session)) -> CommentService:
    return CommentService(CommentRepository(session))


@router.post("/", status_code=201)
async def create_comment(
    data: CreateCommentRequest,
    current_user: UserTable = Depends(get_current_user),
    service: CommentService = Depends(get_comment_service),
):
    return await service.create(
        content=data.content,
        article_id=data.article_id,
        user_id=current_user.id,
        is_verified=current_user.is_verified,
    )


@router.get("/{article_id}")
async def get_comments(
    article_id: uuid.UUID, service: CommentService = Depends(get_comment_service)
):
    return await service.get_by_article_id(article_id)
