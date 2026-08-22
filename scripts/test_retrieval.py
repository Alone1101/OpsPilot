from database import SessionLocal
from services.retrieval_service import retrieve_policies

def test_retrieval():
    db = SessionLocal()

    try:
        results = retrieve_policies(
            db = db,
            query = "Can the system automatically refund RM400?",
        )

        for result in results:
            print(f"\n --- {result.document_name} ---")
            print(result.content)

    finally:
        db.close()

if __name__ == "__main__":
    test_retrieval()