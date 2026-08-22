from pathlib import Path
from database import SessionLocal
from services.embedding_service import embed_text
from db_models import PolicyChunkDB

KNOWLEDGE_DIR = Path("knowledge")

def ingest_policies():
    db = SessionLocal()

    try:
        for file_path in KNOWLEDGE_DIR.glob("*.md"):
            content = file_path.read_text(encoding = "utf-8")

            embedding = embed_text(content)

            chunk = PolicyChunkDB(
                document_name = file_path.name,
                content = content,
                embedding = embedding
            )

            db.add(chunk)

        db.commit()

        print("Policies ingested successfully.")

    finally:
        db.close()

if __name__ == "__main__":
    ingest_policies()