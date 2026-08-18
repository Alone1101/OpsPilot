from fastapi import FastAPI, HTTPException
from models import Order, OrderStatus, CancelOrderResponse, ToolRequest, ToolResponse
from services.order_service import get_order_by_id, cancel_order
from tools.registry import execute_tool
from exceptions import OpsPilotError, OrderNotFoundError, InvalidOrderActionError

app = FastAPI()

orders = {
    "NC-1001": Order(
        id = "NC-1001",
        customer_id = "C-1001",
        status = OrderStatus.DELIVERED,
        total_amount = 129.90
    ),
    "NC-1002": Order(
        id = "NC-1002",
        customer_id = "C-1002",
        status = OrderStatus.SHIPPED,
        total_amount = 4599.00
    ),
    "NC-1003": Order(
        id="NC-1003",
        customer_id="C-1003",
        status=OrderStatus.PROCESSING,
        total_amount=89.00,
    )
}

@app.get("/")
def root():
    return {"message" : "OpsPilot is running"}

@app.get("/orders/{order_id}", response_model = Order)
def get_order(order_id: str):
    try:
        return get_order_by_id(
            orders = orders,
            order_id = order_id
        )

    except OrderNotFoundError as error:
        raise HTTPException(
            status_code = 404,
            detail = str(error)
        )

@app.post("/order/{order_id}/cancel", response_model = CancelOrderResponse)
def cancel_order_endpoint(order_id: str):
    try: 
        return cancel_order(
            orders = orders,
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
def agent_tool(request: ToolRequest):
    try:
        result = execute_tool(orders = orders, tool_name = request.tool, arguments = request.arguments)

        return ToolResponse(success = True, tool = request.tool, result = result.model_dump())

    except OpsPilotError as error:
        return ToolResponse(success = False, tool = request.tool, error = str(error))