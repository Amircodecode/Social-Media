import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class User: 
    email: str
    full_name: str
    username: str
    password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_verified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def validate(self):
        self._validate_name_format()
        self._validate_email()
        self._validate_username()
        
    def _validate_email(self):
        if "@" not in self.email:
            raise ValueError("Некорректный email")
        
    def _validate_name_format(self):
        if not re.match(r'^[a-zа-яё\s]+$', self.full_name):
            raise ValueError("Имя должно содержать только строчные буквы латиницы и кирилицы") 
        
    def can_create_post(self):
        return self.is_verified
    
    def _validate_username(self):
        if not (5 < len(self.username) < 1000):
            raise ValueError("Длина username должна быть от 6 до 999 символов")

def __post_init__(self):
        self.validate()