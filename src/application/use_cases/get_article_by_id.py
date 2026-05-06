class GetArcticleById:
    def __init__(self, article_repository):
        self.article_repository = article_repository

    async def execute(self, id):
        return await self.article_repository.find_by_id(id)
