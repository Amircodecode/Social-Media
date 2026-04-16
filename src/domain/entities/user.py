import uuid
from datetime import datetime

class User:
    def __init__(self, email, full_name, password):
        self.id = uuid.uuid4()
        self.email = email
        self.full_name = full_name.lower()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.password = password
        self.is_verified = False
        
        
