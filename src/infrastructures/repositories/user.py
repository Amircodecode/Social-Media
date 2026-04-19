from ..db.models.user import UserTable
from ...domain.entities.user import User


def save(self, user):
        user_table = UserTable(
            id = user.id,
            email = user.email,
            full_name = user.full_name,
            password = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at,
            is_verified = user.is_verified
        )
        self.db.add(user_table)
        self.db.commit()
        return user