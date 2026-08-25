import time
import statistics
from database import SessionLocal
from services.retrieval_service import retrieve_policies
from evals.rag_cases import RAG_CASES

def run_rag_eval():
    db = SessionLocal()

    recall_at_1 = 0
    recall_at_3 = 0

    latencies = []

    try:
        for case in RAG_CASES:
            start = time.perf_counter()

            results = retrieve_policies(
                db = db,
                query = case["query"],
                limit = 3
            )

            latency = time.perf_counter() - start
            latencies.append(latency)

            documents = [result.document_name for result in results]

            expected = case["expected_document"]

            at_1 = len(documents) > 0 and documents[0] == expected

            at_3 = expected in documents

            recall_at_1 += int(at_1)
            recall_at_3 += int(at_3)

            print(f"\n{case['query']}")
            print(f"  Expected: {expected}")
            print(f"  Retrieved: {documents}")
            print(f"  Recall@1: {at_1}")
            print(f"  Recall@3: {at_3}")
            print(f"  Latency: {latency:.2f}s")

        total = len(RAG_CASES)

        print("\n--- RAG RESULTS ---")

        print(
            f"Recall@1: "
            f"{recall_at_1}/{total} "
            f"({recall_at_1 / total:.1%})"
        )

        print(
            f"Recall@3: "
            f"{recall_at_3}/{total} "
            f"({recall_at_3 / total:.1%})"
        )

        mean_latency = sum(latencies) / len(latencies)
        median_latency = statistics.median(latencies)

        print(f"Mean latency: {mean_latency:.2f}s")

        print(f"Median latency: {median_latency:.2f}s")

    finally:
        db.close()

if __name__ == "__main__":
    run_rag_eval()