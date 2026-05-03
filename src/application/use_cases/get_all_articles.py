class GetAllArticles:
    def __init__(self, user_repository, article_repository):
        self.user_repository = user_repository
        self.article_repository = article_repository
        
    async def execute(self):
        users = await self.user_repository.find_all()
        result = []
        for user in users:
            articles = await self.article_repository.find_by_user_id(user.id)
            result.append({
                "full_name": user.full_name,
                "articles": articles
            })
        return result