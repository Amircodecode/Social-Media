from fastapi import HTTPException


class CreateComment:
    def __init__(self, comment_repository):
        self.comment_repository = comment_repository

    async def execute(self, content, article_id, user_id, is_verified):
        if not is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        return await self.comment_repository.create(
            content=content,
            article_id=article_id,
            user_id=user_id,
        )
