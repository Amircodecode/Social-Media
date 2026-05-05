from src.domain.entities.like import Like

class CreateLike:
    def __init__(self, like_repository):
        self.like_repository = like_repository
        
    # async def execute(self, article_id, user_id)
    #     like = Like()