import uuid
from pydantic import BaseModel, Field


class Like(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    article_id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
