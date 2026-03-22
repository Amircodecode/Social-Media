import re
import uuid
from dataclasses import dataclass, field   
from datetime import datetime, timezone

@dataclass
class Article:
    title: str
    content: str
    author_id: uuid.UUID
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def validate(self):
        self._validate_title()
        self._validate_content()
        
    def _validate_title(self):
        if not (5 < len(self.title) < 1000):
            raise ValueError("Длина заголовка должна быть от 6 до 999 символов")
        if not re.match(r'^[A-Za-zА-ЯЁа-яё\s]+$', self.title):
            raise ValueError("Заголовок должен содержать только строчные буквы латиницы и кирилицы")    
        
    def _validate_content(self):
        if len(self.content) > 10000:
            raise ValueError("Длина статьи должна быть не более 10000 символов")    