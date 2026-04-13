import uuid
from datetime import datetime

class Article:
    def __init__(self, title, content, user_id):
        self.id = uuid.uuid4()
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.updated_at = datetime.now()