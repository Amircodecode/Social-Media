from fastapi import HTTPException


class CommentService:
    def __init__(self, comment_repository):
        self.comment_repository = comment_repository

    async def create(self, content, article_id, user_id, is_verified):
        if not is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        return await self.comment_repository.create(
            content=content,
            article_id=article_id,
            user_id=user_id,
        )

    async def get_by_article_id(self, article_id):
        return await self.comment_repository.find_by_article_id(article_id)

    async def delete(self, id):
        await self.comment_repository.delete(id)
