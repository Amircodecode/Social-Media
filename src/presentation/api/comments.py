from fastapi import APIRouter, Depends
from src.infrastructures.auth.dependencies import get_current_user
import uuid
from src.domain.entities.user import User
from src.application.use_cases.create_comment import CreateComment
from src.infrastructures.repositories.comment import CommentRepository

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/")
async def create_comment(
    content: str, article_id: uuid.UUID, current_user=Depends(get_current_user)
):
    comment_repository = CommentRepository()
    use_case = CreateComment(comment_repository)
    return await use_case.execute(
        content=content,
        article_id=article_id,
        user_id=current_user.id,
        is_verified=current_user.is_verified,
    )


@router.get("/{article_id}")
async def get_comments(article_id: uuid.UUID):
    comment_repository = CommentRepository()
    return await comment_repository.find_by_article_id(article_id)


@router.delete("/delete/{id}")
async def delete_comment(id: uuid.UUID, current_user: User = Depends(get_current_user)):
    comment_repository = CommentRepository()
    await comment_repository.delete(id)
    return {"message": "Comment deleted successfully!!"}
