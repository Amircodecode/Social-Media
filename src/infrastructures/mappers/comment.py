from ..db.models.comment import CommentTable
from ...domain.entities.comment import Comment

def to_entity(model):
    return Comment(
        id = model.id,
        user_id = model.user_id,
        article_id = model.article_id,
        content = model.content,
        created_at = model.created_at
    )
    
def to_model(entity):
    return CommentTable(
        id = entity.id,
        user_id = entity.user_id,
        article_id = entity.article_id,
        content = entity.content,
        created_at = entity.created_at
    )