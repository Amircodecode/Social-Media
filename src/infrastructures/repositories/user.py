from ..db.database import SessionLocal
from ..db.models.user import UserTable
from ..mappers.user import to_model, to_entity
from ...domain.entities.user import User

class UserRepository:
    async def save(self, user: User):
        async with SessionLocal() as session:
            model = to_model(user)
            session.add(model)
            await session.commit()
            return to_entity(model)    
    
    def find_by_email(self, email):
        pass
        
    def find_by_id(self, id):
        pass
    def delete(self, user):
        pass
        
    def update(self, user):
        pass