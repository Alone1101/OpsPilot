from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import Order, OrderStatus, CancelOrderResponse, ToolRequest, ToolResponse, AgentRequest, PolicyQuestionRequest, PolicyAnswerResponse, PolicyAgentResponse, ToolAgentResponse
from services.order_service import get_order_by_id, cancel_order
from services.rag_service import answer_policy_question
from tools.registry import execute_tool
from exceptions import OpsPilotError, OrderNotFoundError, InvalidOrderActionError
from agents.agent_service import process_message
from database import get_db
from logging_config import configure_logging

configure_logging()

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "OpsPilot is running"}

@app.get("/orders/{order_id}", response_model = Order)
def get_order(order_id: str, db: Session = Depends(get_db)):
    try:
        order = get_order_by_id(
            db = db,
            order_id = order_id
        )

        return Order(
            id = order.id,
            customer_id = order.customer_id,
            status = OrderStatus(order.status),
            total_amount = order.total_amount
        )

    except OrderNotFoundError as error:
        raise HTTPException(
            status_code = 404,
            detail = str(error)
        )

@app.post("/orders/{order_id}/cancel", response_model = CancelOrderResponse)
def cancel_order_endpoint(order_id: str, db : Session = Depends(get_db)):
    try: 
        return cancel_order(
            db = db,
            order_id = order_id
        )

    except OrderNotFoundError as error:
        raise HTTPException(
            status_code = 404,
            detail = str(error)
        )

    except InvalidOrderActionError as error:
        raise HTTPException(
            status_code = 400,
            detail = str(error)
        )

@app.post("/agent/tool", response_model = ToolResponse)
def agent_tool(request: ToolRequest, db: Session = Depends(get_db)):
    try:
        result = execute_tool(
            db = db,
            tool_name = request.tool,
            arguments = request.arguments
        )

        return ToolResponse(
            success = True,
            tool = request.tool,
            result = result.model_dump()
        )

    except OpsPilotError as error:
        return ToolResponse(
            success = False,
            tool = request.tool,
            error = str(error)
        )

@app.post("/agent/message", response_model = PolicyAgentResponse | ToolAgentResponse)
def agent_message(request: AgentRequest, db: Session = Depends(get_db)):
    return process_message(
        message = request.message,
        db = db
    )

@app.post("/policy/ask", response_model = PolicyAnswerResponse)
def ask_policy(request: PolicyQuestionRequest, db: Session = Depends(get_db)):
    answer = answer_policy_question(
        db = db,
        question = request.question
    )

    return PolicyAnswerResponse(answer = answer)

app.mount("/ui", StaticFiles(directory = "static", html = True), name = "static")