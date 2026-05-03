from ..db.models.article import ArticleTable
from ...domain.entities.article import Article

def to_entity(model):   
    return Article(
        id = model.id,
        user_id = model.user_id,
        title = model.title,
        content = model.content,
        created_at = model.created_at,
        updated_at = model.updated_at
    )
    
def to_model(entity):
    return ArticleTable(
        id = entity.id,
        user_id = entity.user_id,
        title = entity.title,
        content = entity.content,
        created_at = entity.created_at,
        updated_at = entity.updated_at
    )