from fastapi import APIRouter, Depends
from src.application.use_cases.create_article import CreateArticle
from src.infrastructures.repositories.article import ArticleRepository
from src.infrastructures.auth.dependencies import get_current_user
from src.application.use_cases.get_all_articles import GetAllArticles
from src.infrastructures.repositories.user import UserRepository
import uuid
from src.application.use_cases.get_article_by_id import GetArcticleById
from src.domain.entities.user import User
from src.infrastructures.repositories.like import LikeRepository
from src.infrastructures.auth.password import verify_password


router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
async def create_post(title: str, content: str, current_user=Depends(get_current_user)):
    article_repository = ArticleRepository()
    use_case = CreateArticle(article_repository)
    return await use_case.execute(title=title, content=content, user_id=current_user.id, is_verified=current_user.is_verified)

@router.get("/all")
async def get_all_posts():
    user_repository = UserRepository()
    article_repository = ArticleRepository()
    like_repository = LikeRepository()
    use_case = GetAllArticles(user_repository, article_repository, like_repository)
    return await use_case.execute()

@router.get("/{id}")
async def get_post(id: uuid.UUID):
    article_repository = ArticleRepository()
    use_case = GetArcticleById(article_repository)
    return await use_case.execute(id)
    
@router.delete("/delete/{id}")
async def delete_user(id: uuid.UUID, current_user: User = Depends(get_current_user)):
    article_repository = ArticleRepository()
    await article_repository.delete(id)
    return {"message": "Posts deleted successfully!!"}

@router.put("/update/{id}")
async def update_post(id: uuid.UUID, title: str, content: str, current_user: User = Depends(get_current_user)):
    article_repository = ArticleRepository()
    article = await article_repository.find_by_id(id)
    if article.user_id != current_user.id:
        return {"error": "You are not authorized to update this post"}
    article.title = title
    article.content = content
    updated_article = await article_repository.update(id, article)
    return updated_article
    
       

    
