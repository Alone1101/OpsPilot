from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Order, OrderStatus, CancelOrderResponse, ToolRequest, ToolResponse, AgentRequest
from services.order_service import get_order_by_id, cancel_order
from tools.registry import execute_tool
from exceptions import OpsPilotError, OrderNotFoundError, InvalidOrderActionError
from agents.agent_service import process_message
from database import get_db

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

@app.post("/agent/message", response_model = ToolResponse)
def agent_message(request: AgentRequest, db: Session = Depends(get_db)):
    try:
        return process_message(
            message = request.message,
            db = db
        )

    except OpsPilotError as error:
        return ToolResponse(
            success = False,
            tool = "unknown",
            error = str(error)
        )