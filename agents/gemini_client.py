from google import genai
from google.genai import types
from dotenv import load_dotenv
from models import AgentDecision, RequestClassification

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

            escalate_case
            - Escalate an order issue for human review.
            - Use when autonomous action is unsafe or not permitted.
            - Requires: order_id, reason
            - Optional: priority

            Select one appropriate tool based on the user's request and extract the order ID.
            Do not invent tools.
            """,

            response_mime_type = "application/json",
            response_schema = AgentDecision
        )
    )

    return response.parsed

def classify_request(message: str) -> RequestClassification:
    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = message,
        config = types.GenerateContentConfig(
            system_instruction = """
            Classify the user request

            ACTION:
            The user wants OpsPolit to perform or attempt an operation, such as cancelling, refunding, tracking, checking eligibility, or escalating a case.

            POLICY_QUESTION:
            The user is asking about company policy, rules, or what is allowed.

            Return only the classification.
            """,

            response_mime_type = "application/json",
            response_schema = RequestClassification
        ),
    )

    return response.parsed