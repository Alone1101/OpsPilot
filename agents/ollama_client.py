import os
import json
import requests
import logging
from pydantic import ValidationError
from dotenv import load_dotenv
from models import RequestClassification, AgentDecision
from exceptions import LLMUnavailableError, LLMResponseError

load_dotenv()

logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def _generate(prompt: str) -> str:
    logger.info("Using Ollama model: %s", OLLAMA_MODEL)

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0}
            },
            timeout = 120
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise LLMUnavailableError(f"Ollama request failed: {error}")

    try:
        data = response.json()
        return data["response"]

    except (ValueError, KeyError) as error:
        raise LLMResponseError("Ollama returned an invalid response") from error

def classify_request(message: str) -> RequestClassification:
    prompt = f"""
    Classify the following customer request.

    ACTION:
    The request concerns a specific customer order or case and requires retrieving current state or performing/attempting an operation.
    If the message contains a specific order ID and asks about that order's status, tracking, cancellation, refund eligibility, refund execution, or escalation, classify it as ACTION.

    POLICY_QUESTION:
    The request asks about general company policy, rules, limits, or what is allowed, without requiring lookup of a specific customer's current order state.

    Examples:
    - "Can I get a refund for order NC-1003?" -> ACTION
    - "Is NC-1003 eligible for a refund?" -> ACTION
    - "What is your refund policy?" -> POLICY_QUESTION
    - "Are refunds above RM250 allowed automatically?" -> POLICY_QUESTION

    Return ONLY valid JSON in this exact format:

    {{"request_type": "ACTION"}}

    Allowed request_type values:
    - ACTION
    - POLICY_QUESTION

    Request:
    {message}
    """

    raw = _generate(prompt)

    try:
        data = json.loads(raw)

        return RequestClassification(**data)

    except (json.JSONDecodeError, ValidationError) as error:
        raise LLMResponseError("Invalid classification response from Ollama") from error

def decide_tool(message: str) -> AgentDecision:
    prompt = f"""
    You are the decision component of OpsPilot.

    Available tools:

    get_order
    - Retrieve general order details such as customer, total amount, or current record.
    - Use only when the user asks for general order information.
    - Requires: order_id

    get_tracking_status
    - Use when the user asks where an order is, whether it has shipped, delivery progress, transit state, or shipment status.
    - Requires: order_id

    cancel_order
    - Use when the user explicitly asks to cancel or stop an order.
    - Requires: order_id

    check_refund_eligibility
    - Use when the user asks whether a specific order can receive a refund.
    - Do not use issue_refund unless the user actually asks to perform the refund.
    - Requires: order_id

    issue_refund
    - Use when the user explicitly asks to issue, process, or give a refund.
    - Requires: order_id, amount

    escalate_case
    - Use when the user explicitly asks for human review/escalation.
    - Requires: order_id
    - reason and priority may be provided when available.

    Do not invent tools.

    Return ONLY valid JSON.

    Format:

    {{
    "tool": "tool_name",
    "order_id": "NC-1001",
    "amount": null,
    "reason": null,
    "priority": null
    }}

    Rules:
    - Amount must be a JSON number only.
    - Do not include currency symbols or text in amount.
    - Example: RM50 must be returned as 50.0.
    - Use null when amount is not provided.

    User request:
    {message}
    """

    raw = _generate(prompt)
    data = json.loads(raw)
    return AgentDecision(**data)

def generate_text(prompt: str) -> str:
    return _generate(prompt)