from src.domain.entities.user import User
from src.infrastructures.auth.password import hash_password

class RegisterUser:
    def __init__(self, repository):
        self.repository = repository
    
    async def execute(self, email, full_name, password):
        hashed_password = hash_password(password)
        user = User(email=email, full_name=full_name, password=hashed_password)
        return await self.repository.save(user)