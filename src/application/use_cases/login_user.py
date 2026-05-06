from src.infrastructures.auth.password import verify_password
from src.infrastructures.auth.jwt import create_access_token


class LoginUser:
    def __init__(self, repository):
        self.repository = repository

    async def execute(self, email, password):
        user = await self.repository.find_by_email(email)
        if user and verify_password(password, user.password):
            return create_access_token({"sub": str(user.id)})
        return None
