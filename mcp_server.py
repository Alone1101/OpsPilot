from services.order_service import get_order_by_id, get_tracking_status
from database import SessionLocal
from mcp.server import MCPServer

mcp = MCPServer("OpsPilot", instructions = ("OpsPilot provides customer operations tools for order support."))

@mcp.tool()
def get_order(order_id: str) -> dict:
    "Retrieve details for a specific order."

    db = SessionLocal()

    try:
        order = get_order_by_id(
            db = db,
            order_id = order_id
        )

        return {
            "id": order.id,
            "customer_id": order.customer_id,
            "status": order.status,
            "total_amount": order.total_amount,
        }

    finally:
        db.close()

@mcp.tool()
def get_tracking_status_mcp(order_id: str) -> dict:
    "Retrieve the current tracking status for a specific order."

    db = SessionLocal()

    try:
        result = get_tracking_status(
            db = db,
            order_id = order_id
        )

        return {
            "order_id": result.order_id,
            "status": result.status,
            "message": result.message
        }

    finally:
        db.close()

if __name__ == "__main__":
    mcp.run (
        transport = "streamable-http",
        host = "127.0.0.1",
        port = 8001
    )