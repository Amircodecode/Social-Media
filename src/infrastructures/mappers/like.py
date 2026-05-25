from src.infrastructures.db.models.like import LikeTable
from src.domain.entities.like import Like


def to_entity(model):
    return Like(id=model.id, article_id=model.article_id, user_id=model.user_id)


def to_model(entity):
    return LikeTable(id=entity.id, article_id=entity.article_id, user_id=entity.user_id)
