import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class Comment(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID
    article_id: uuid.UUID
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"from_attributes": True}
