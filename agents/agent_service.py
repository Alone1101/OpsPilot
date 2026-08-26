import logging
import time
import uuid
from sqlalchemy.orm import Session
from models import PolicyAgentResponse, ToolAgentResponse 
from agents.graph import build_agent_graph
from exceptions import OpsPilotError

logger = logging.getLogger(__name__)

def process_message(message: str, db: Session) -> PolicyAgentResponse | ToolAgentResponse:
    graph = build_agent_graph(db)

    request_id = str(uuid.uuid4())
    started_at = time.perf_counter()

    try:
        state = graph.invoke({
            "message": message,
            "request_id": request_id,
            "started_at": started_at
        })

        latency = time.perf_counter() - started_at

        logger.info("[%s] Request completed in %.2fs", request_id, latency)

    except OpsPilotError as error:
        return ToolAgentResponse(
            tool = "system",
            error = str(error)
        )

    if "answer" in state:
        return PolicyAgentResponse(answer = state["answer"])

    return ToolAgentResponse(
        tool = state["tool"],
        result = state.get("result"),
        error = state.get("error")
    )