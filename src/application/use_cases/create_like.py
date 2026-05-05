from src.domain.entities.like import Like
from fastapi import HTTPException

class CreateLike:
    def __init__(self, like_repository, article_repository):
        self.like_repository = like_repository
        self.article_repository = article_repository
    
    async def execute(self, article_id, user_id, is_verified):
        article = await self.article_repository.find_by_id(article_id)
        if article.user_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot like your own post")
        like = Like(article_id=article_id, user_id=user_id)
        return await self.like_repository.save(like)