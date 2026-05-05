from fastapi import APIRouter, Depends
from src.infrastructures.auth.dependencies import get_current_user
import uuid
from src.domain.entities.user import User
from src.application.use_cases.create_like import CreateLike
from src.infrastructures.repositories.like import LikeRepository
from src.infrastructures.repositories.article import ArticleRepository

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/")
async def create_like(article_id: uuid.UUID, current_user=Depends(get_current_user)):
    like_repository = LikeRepository()
    article_repository = ArticleRepository()
    use_case = CreateLike(like_repository, article_repository)
    return await use_case.execute(article_id=article_id, user_id=current_user.id, is_verified=current_user.is_verified)

@router.delete("/delete/{id}")
async def delete_like(id: uuid.UUID, current_user: User = Depends(get_current_user)):
    like_repository = LikeRepository()
    await like_repository.delete(id)
    return {"message": "Like deleted successfully!!"}