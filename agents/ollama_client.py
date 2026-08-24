import os
import json
import requests
from dotenv import load_dotenv
from models import RequestClassification, AgentDecision

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

def _generate(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout = 120
    )

    response.raise_for_status()

    data = response.json()
    return data["response"]

def classify_request(message: str) -> RequestClassification:
    prompt = f"""
    Classify the following customer request.

    Return ONLY valid JSON in this exact format:

    {{"request_type": "ACTION"}}

    Allowed request_type values:
    - ACTION
    - POLICY_QUESTION

    Request:
    {message}
    """

    raw = _generate(prompt)
    data = json.loads(raw)

    return RequestClassification(**data)

def decide_tool(message: str) -> AgentDecision:
    prompt = f"""
    You are the decision component of OpsPilot.

    Available tools:

    get_order
    get_tracking_status
    cancel_order
    check_refund_eligibility
    issue_refund
    escalate_case

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