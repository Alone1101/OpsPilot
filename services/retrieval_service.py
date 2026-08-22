from sqlalchemy.orm import Session
from services.embedding_service import embed_text
from db_models import PolicyChunkDB

def retrieve_policies(db: Session, query: str, limit: int = 3) -> list[PolicyChunkDB]:
    query_embedding = embed_text(query)

    results = (db.query(PolicyChunkDB).order_by(PolicyChunkDB.embedding.cosine_distance(query_embedding)).limit(limit).all())

    return results