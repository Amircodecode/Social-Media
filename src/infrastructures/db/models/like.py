from sqlalchemy import Column, String, Text, Boolean, ForeignKey
from ..base import Base
import uuid
from sqlalchemy.sql import func 
from sqlalchemy.dialects.postgresql import UUID

class LikeTable(Base):
    __tablename__ = "likes"
    
    id = Column(UUID, default = uuid.uuid4(), primary_key = True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable = False)
    article_id = Column(UUID, ForeignKey("articles.id"), nullable = False)