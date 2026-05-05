class GetAllArticles:
    def __init__(self, user_repository, article_repository, like_repository):
        self.user_repository = user_repository
        self.article_repository = article_repository
        self.like_repository = like_repository

    async def execute(self):
        users = await self.user_repository.find_all()
        result = []
        for user in users:
            articles = await self.article_repository.find_by_user_id(user.id)
            articles_with_likes = []
            for article in articles:
                likes = await self.like_repository.find_by_article_id(article.id)
                articles_with_likes.append({
                    "id": article.id,
                    "title": article.title,
                    "content": article.content,
                    "likes": [{"id": like.id, "user_id": like.user_id} for like in likes]
                })
            result.append({
                "full_name": user.full_name,
                "articles": articles_with_likes
            })
        return result