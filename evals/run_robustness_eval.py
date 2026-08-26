from database import SessionLocal
from agents.graph import build_agent_graph
from evals.robustness_cases import ROBUSTNESS_CASES

def run_robustness_eval():
    db = SessionLocal()

    passed = 0
    total = len(ROBUSTNESS_CASES)

    try:
        graph = build_agent_graph(db)

        for case in ROBUSTNESS_CASES:
            state = graph.invoke({"message": case["message"]})

            error = state.get("error") or ""

            expected = case["expected_error_contains"]

            case_passed = (expected.lower() in error.lower())

            passed += int(case_passed)

            print(f"\n{case['message']}")
            print(f"  Expected error contains: {expected}")
            print(f"  Actual error:            {error}")
            print(f"  Passed:                  {case_passed}")

        print("\n--- ROBUSTNESS RESULTS ---")

        print(
            f"Handled correctly: "
            f"{passed}/{total} "
            f"({passed / total:.1%})"
        )

    finally:
        db.close()

if __name__ == "__main__":
    run_robustness_eval()