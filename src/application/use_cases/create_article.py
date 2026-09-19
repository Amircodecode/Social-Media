from fastapi import HTTPException


class CreateArticle:
    def __init__(self, article_repository):
        self.article_repository = article_repository

    async def execute(self, title, content, user_id, is_verified):
        if not is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        return await self.article_repository.create(
            title=title,
            content=content,
            user_id=user_id,
        )
