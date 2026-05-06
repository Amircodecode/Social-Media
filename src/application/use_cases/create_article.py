from src.domain.entities.article import Article
from fastapi import HTTPException
import re


class CreateArticle:
    def __init__(self, article_repository):
        self.article_repository = article_repository

    async def execute(self, title, content, user_id, is_verified):
        if not is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")
        if len(title) < 5 or len(title) > 1000:
            raise HTTPException(
                status_code=400, detail="Title must be between 5 and 1000 characters"
            )
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s]+$", title):
            raise HTTPException(
                status_code=400, detail="Title must contain only letters"
            )
        if len(content) > 10000:
            raise HTTPException(
                status_code=400, detail="Content must be less than 10000 characters"
            )
        article = Article(title=title, content=content, user_id=user_id)
        return await self.article_repository.save(article)
