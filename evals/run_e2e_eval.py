from database import SessionLocal
from db_models import OrderDB, EscalationDB
from agents.graph import build_agent_graph
from evals.e2e_cases import E2E_CASES

def reset_test_state(db):
    order = db.get(OrderDB, "NC-1003")

    if order is not None:
        order.status = "PROCESSING"

    db.query(EscalationDB).delete()

    db.commit()

def run_e2e_eval():
    db = SessionLocal()

    passed = 0
    total = len(E2E_CASES)

    try:
        reset_test_state(db)

        graph = build_agent_graph(db)

        for case in E2E_CASES:
            state = graph.invoke({"message": case["message"]})

            case_passed = True

            if state.get("tool") != case["expected_tool"]:
                case_passed = False

            if "expected_order_status" in case:
                order = db.get(
                    OrderDB,
                    state["arguments"]["order_id"]
                )

                if order.status != case["expected_order_status"]:
                    case_passed = False

            if "expected_escalation_status" in case:
                escalation = (db.query(EscalationDB).filter(EscalationDB.order_id == state["arguments"]["order_id"]).order_by(EscalationDB.id.desc()).first())

                if (escalation is None or escalation.status != case["expected_escalation_status"]):
                    case_passed = False

            passed += int(case_passed)

            print(f"\n{case['name']}")
            print(f"  Tool:   {state.get('tool')}")
            print(f"  Passed: {case_passed}")

        print("\n--- E2E RESULTS ---")

        print(
            f"Workflows passed: "
            f"{passed}/{total} "
            f"({passed / total:.1%})"
        )

    finally:
        db.close()

if __name__ == "__main__":
    run_e2e_eval()