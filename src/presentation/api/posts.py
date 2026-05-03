from fastapi import APIRouter, Depends
from src.application.use_cases.create_article import CreateArticle
from src.infrastructures.repositories.article import ArticleRepository
from src.infrastructures.auth.dependencies import get_current_user
from src.application.use_cases.get_all_articles import GetAllArticles
from src.infrastructures.repositories.user import UserRepository

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/")
async def create_post(title: str, content: str, current_user=Depends(get_current_user)):
    article_repository = ArticleRepository()
    use_case = CreateArticle(article_repository)
    return await use_case.execute(title=title, content=content, user_id=current_user.id)

@router.get("/all")
async def get_all_posts():
    user_repository = UserRepository()
    article_repository = ArticleRepository()
    use_case = GetAllArticles(user_repository, article_repository)
    return await use_case.execute()