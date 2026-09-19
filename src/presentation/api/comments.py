import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructures.auth.dependencies import get_current_user
from src.application.use_cases.create_comment import CreateComment
from src.infrastructures.repositories.comment import CommentRepository
from src.infrastructures.db.database import get_session
from src.infrastructures.db.models.user import UserTable  # заменили User

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", status_code=201)
async def create_comment(
    content: str,
    article_id: uuid.UUID,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    comment_repository = CommentRepository(session)
    use_case = CreateComment(comment_repository)
    return await use_case.execute(
        content=content,
        article_id=article_id,
        user_id=current_user.id,
        is_verified=current_user.is_verified,
    )


@router.get("/{article_id}")
async def get_comments(
    article_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    comment_repository = CommentRepository(session)
    return await comment_repository.find_by_article_id(article_id)


@router.delete("/delete/{id}")
async def delete_comment(
    id: uuid.UUID,
    current_user: UserTable = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    comment_repository = CommentRepository(session)
    await comment_repository.delete(id)
    return {"message": "Comment deleted successfully!!"}
