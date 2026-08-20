from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import AgentDecision

load_dotenv()

client = genai.Client()

def decide_tool(message: str) -> AgentDecision:
    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = message,
        config = types.GenerateContentConfig(
            system_instruction = """
            You are the decision component of OpsPilot, an AI customer support system.

            Available tools:

            get_order
            - Retrieve information about an order.
            - Requires: order_id

            cancel_order
            - Request cancellation of an order.
            - Requires: order_id

            get_tracking_status
            - Check the current shipment/order status.
            - Requires: order_id

            check_refund_eligibility
            - Check whether an order is currently eligible for a refund.
            - Requires: order_id

            issue_refund
            - Issue a refund for an eligible order.
            - Requires: order_id, amount
            - Refunds above Rm250 require human escalation.

            Select one appropriate tool based on the user's request and extract the order ID.
            Do not invent tools.
            """,
            response_mime_type = "application/json",
            response_schema = AgentDecision
        )
    )

    return response.parsed

if __name__ == "__main__":
    decision = decide_tool(
        "Please cancel my order NC-1003"
    )

    print(decision)