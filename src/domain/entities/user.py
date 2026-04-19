import uuid
from datetime import datetime

class User:
    def __init__(self, email, full_name, password, id = None, created_at = None, updated_at = None, is_verified = None):
        self.id = id if id is not None else uuid.uuid4()
        self.email = email
        self.full_name = full_name.lower()
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.password = password
        self.is_verified = is_verified if is_verified is not None else False
        
        
