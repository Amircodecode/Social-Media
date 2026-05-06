import uuid
from datetime import datetime


class Article:
    def __init__(
        self, title, content, user_id, id=None, created_at=None, updated_at=None
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
