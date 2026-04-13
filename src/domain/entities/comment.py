from datetime import datetime
import uuid

class Comment:
    def __init__(self, user_id, article_id, content):
       self.id = uuid.uuid4()
       self.user_id = user_id
       self.article_id = article_id
       self.content = content
       self.created_at = datetime.now()