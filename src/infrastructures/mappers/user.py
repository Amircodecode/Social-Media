from src.infrastructures.db.models.user import UserTable
from src.domain.entities.user import User


def to_entity(model):
    return User(
        id=model.id,
        email=model.email,
        is_verified=model.is_verified,
        full_name=model.full_name,
        password=model.password,
        created_at=model.created_at,
        updated_at=model.updated_at,
        verification_token=model.verification_token,
        token_expires_at=model.token_expires_at,
    )


def to_model(entity):
    return UserTable(
        id=entity.id,
        email=entity.email,
        is_verified=entity.is_verified,
        full_name=entity.full_name,
        password=entity.password,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        verification_token=entity.verification_token,
        token_expires_at=entity.token_expires_at,
    )
