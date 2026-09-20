from fastapi import HTTPException


class ArticleService:
    def __init__(self, article_repository, like_repository, user_repository):
        self.article_repository = article_repository
        self.like_repository = like_repository
        self.user_repository = user_repository

    async def get_all(
        self, page=1, limit=10, search=None, date_from=None, date_to=None
    ):
        users = await self.user_repository.find_all()
        result = []
        for user in users:
            articles = await self.article_repository.find_by_user_id(user.id)
            articles_with_likes = []
            for article in articles:
                if search and search.lower() not in article.title.lower():
                    continue
                if date_from and article.created_at < date_from:
                    continue
                if date_to and article.created_at > date_to:
                    continue
                likes = await self.like_repository.find_by_article_id(article.id)
                articles_with_likes.append(
                    {
                        "id": article.id,
                        "title": article.title,
                        "content": article.content,
                        "likes": [
                            {"id": like.id, "user_id": like.user_id} for like in likes
                        ],
                    }
                )
            result.append(
                {"full_name": user.full_name, "articles": articles_with_likes}
            )

        start = (page - 1) * limit
        end = start + limit
        return result[start:end]

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
