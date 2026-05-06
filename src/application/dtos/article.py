from pydantic import BaseModel
from datetime import datetime
import uuid


class ArticleResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
