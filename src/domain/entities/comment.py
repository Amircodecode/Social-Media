from datetime import datetime
import uuid

class Comment:
    def __init__(self, user_id, article_id, content, id = None, created_at = None):
       self.id = id if id is not None else uuid.uuid4()
       self.user_id = user_id
       self.article_id = article_id
       self.content = content
       self.created_at = created_at if created_at is not None else datetime.now()