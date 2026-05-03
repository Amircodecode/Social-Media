from src.domain.entities.article import Article

class CreateArticle:
    def __init__(self, article_repository):
        self.article_repository = article_repository

    async def execute(self, title, content, user_id):
        article = Article(title=title, content=content, user_id=user_id)
        return await self.article_repository.save(article)