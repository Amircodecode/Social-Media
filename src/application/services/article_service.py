from fastapi import HTTPException


class ArticleService:
    def __init__(self, article_repository, like_repository, user_repository):
        self.article_repository = article_repository
        self.like_repository = like_repository
        self.user_repository = user_repository

    async def get_all(
        self, page=1, limit=10, search=None, date_from=None, date_to=None
    ):
        offset = (page - 1) * limit
        articles = await self.article_repository.find_all_with_filters(
            search=search,
            date_from=date_from,
            date_to=date_to,
            limit=limit,
            offset=offset,
        )

        grouped: dict = {}
        order: list = []
        for article in articles:
            user = article.user
            if user.id not in grouped:
                grouped[user.id] = {"full_name": user.full_name, "articles": []}
                order.append(user.id)

            likes = await self.like_repository.find_by_article_id(article.id)
            grouped[user.id]["articles"].append(
                {
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "likes": [
                        {"id": like.id, "user_id": like.user_id} for like in likes
                    ],
                }
            )

        return [grouped[user_id] for user_id in order]

    async def get_by_id(self, id):
        article = await self.article_repository.find_by_id(id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article

    async def delete(self, id, current_user_id):
        article = await self.article_repository.find_by_id(id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        if article.user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to delete this post"
            )
        await self.article_repository.delete(id)

    async def update(self, id, current_user_id, title, content):
        article = await self.article_repository.find_by_id(id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        if article.user_id != current_user_id:
            raise HTTPException(
                status_code=403, detail="You are not authorized to update this post"
            )
        return await self.article_repository.update(id, title=title, content=content)

    async def create(self, title, content, user_id, is_verified):
        if not is_verified:
            raise HTTPException(status_code=403, detail="Email not verified")

        return await self.article_repository.create(
            title=title,
            content=content,
            user_id=user_id,
        )
