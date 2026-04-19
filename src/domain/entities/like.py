import uuid
from datetime import datetime

class Like:
    def __init__(self, article_id, user_id, id = None):
        self.id = id if id is not None else uuid.uuid4()
        self.article_id = article_id
        self.user_id = user_id