from src.domain.entities.comment import Comment

class CreateComment:
    def __init__(self, comment_repository):
        self.comment_repository = comment_repository
        
    async def execute(self, content, article_id, user_id):
        comment = Comment(content=content, article_id=article_id, user_id=user_id)
        return await self.comment_repository.save(comment)