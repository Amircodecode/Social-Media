from fastapi import HTTPException


class LikeService:
    def __init__(self, like_repository, article_repository):
        self.like_repository = like_repository
        self.article_repository = article_repository

    async def create(self, article_id, user_id, is_verified):
        article = await self.article_repository.find_by_id(article_id)

        if article is None:
            raise HTTPException(status_code=404, detail="Article not found")

        if article.user_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot like your own post")

        return await self.like_repository.save(
            article_id=article_id,
            user_id=user_id,
        )

    async def delete(self, like_id, current_user_id):
        like = await self.like_repository.find_by_id(like_id)
        if not like:
            raise HTTPException(status_code=404, detail="Like not found")
        if like.user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to delete this like"
            )
        await self.like_repository.delete(like_id)
