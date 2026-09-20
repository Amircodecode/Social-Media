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

    async def delete(self, article_id, comment_id, current_user_id):
        comment = await self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.article_id != article_id:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.user_id != current_user_id:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to delete this comment",
            )
        await self.comment_repository.delete(comment_id)
