from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from ..base import Base
import uuid
from sqlalchemy.sql import func 
from sqlalchemy.dialects.postgresql import UUID

class ArticleTable(Base):
    __tablename__ = "articles"
    
    id = Column(UUID, default = uuid.uuid4(), primary_key = True, nullable = False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable = False)
    title = Column(Text, nullable = False)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, nullable = False, default = func.now())   
    updated_at = Column(DateTime, nullable = False, default = func.now())