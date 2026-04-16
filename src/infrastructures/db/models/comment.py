from sqlalchemy import Column, Text, String, DateTime, ForeignKey
from ..base import Base
import uuid 
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class commentTable(Base):
    __tablename__ = "comments"
    
    id = Column(UUID, primary_key = True)
    article_id = Column(UUID, primary_key = True)
    content = Column(Text, nullable = False)
    created_at = Column(DateTime, nullable = False, default = func.now())
    