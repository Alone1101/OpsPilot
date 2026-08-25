import sys
import time
import statistics
from database import SessionLocal
from agents.graph import build_agent_graph
from evals.dev_cases import DEV_CASES
from evals.test_cases import TEST_CASES

def run_eval():
    mode =sys.argv[1] if len(sys.argv) > 1 else "dev"

    if mode == "test":
        cases = TEST_CASES
    else:
        cases = DEV_CASES
    
    db = SessionLocal()

    total = len(cases)

    request_type_correct = 0
    tool_correct = 0
    order_id_correct = 0
    amount_correct = 0

    latencies = []

    try:
        graph = build_agent_graph(db)

        # Warm up LLM so model loading time is not included in benchmark latency
        graph.invoke({"message": "Track order NC-1002"})

        for case in cases:

            start = time.perf_counter()

            state = graph.invoke({"message": case["message"]})

            latency = time.perf_counter() - start
            latencies.append(latency)

            actual_request_type = state.get("request_type")
            actual_tool = state.get("tool")

            arguments = state.get("arguments") or {}

            actual_order_id = arguments.get("order_id")
            actual_amount = arguments.get("amount")

            request_type_ok = (actual_request_type is not None and actual_request_type.value == case["expected_request_type"])

            tool_ok = (actual_tool == case["expected_tool"])

            order_id_ok = (actual_order_id == case.get("expected_order_id"))

            expected_amount = case.get("expected_amount")

            amount_ok = actual_amount == expected_amount

            request_type_correct += int(request_type_ok)
            tool_correct += int(tool_ok)
            order_id_correct += int(order_id_ok)
            amount_correct += int(amount_ok)

            print(f"\n{case['message']}")
            print(f"  Request type: {request_type_ok}")
            print(f"  Tool:         {tool_ok}")
            print(f"  Order ID:     {order_id_ok}")
            print(f"  Amount:       {amount_ok}")
            print(f"  Latency:      {latency:.2f}s")

            if not request_type_ok:
                print(f"  Expected request type: {case['expected_request_type']}")
                print(f"  Actual request type:   {actual_request_type}")

            if not tool_ok:
                print(f"  Expected tool: {case['expected_tool']}")
                print(f"  Actual tool:   {actual_tool}")

            if not order_id_ok:
                print(f"  Expected order ID: {case.get('expected_order_id')}")
                print(f"  Actual order ID:   {actual_order_id}")

        print("\n--- RESULTS ---")

        print(
            f"Request classification: "
            f"{request_type_correct}/{total} "
            f"({request_type_correct / total:.1%})"
        )

        print(
            f"Tool selection: "
            f"{tool_correct}/{total} "
            f"({tool_correct / total:.1%})"
        )

        print(
            f"Order ID extraction: "
            f"{order_id_correct}/{total} "
            f"({order_id_correct / total:.1%})"
        )

        print(
            f"Amount extraction: "
            f"{amount_correct}/{total} "
            f"({amount_correct / total:.1%})"
        )

        mean_latency = sum(latencies) / len(latencies)
        median_latency = statistics.median(latencies)

        print(f"Mean latency: {mean_latency:.2f}s")

        print(f"Median latency: {median_latency:.2f}s")

    finally:
        db.close()

if __name__ == "__main__":
    run_eval()