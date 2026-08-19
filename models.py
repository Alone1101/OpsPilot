from enum import Enum
from pydantic import BaseModel
from typing import Any

class OrderStatus(str, Enum):
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Order(BaseModel):
    id: str
    customer_id: str
    status: OrderStatus
    total_amount: float

class CancelOrderResponse(BaseModel):
    order_id: str
    status: OrderStatus
    message: str

class ToolRequest(BaseModel):
    tool: str
    arguments: dict[str, Any]

class ToolResponse(BaseModel):
    success: bool
    tool: str
    result: dict[str, Any] | None = None
    error: str | None = None

class AgentDecision(BaseModel):
    tool: str
    order_id: str

class AgentRequest(BaseModel):
    message: str