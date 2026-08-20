from database import SessionLocal
from db_models import OrderDB

def seed_orders():
    db = SessionLocal()

    try:
        existing = db.query(OrderDB).count()

        if existing > 0:
            print("Orders already exist. Skipping seed.")
            return

        orders = [
            OrderDB(
                id="NC-1001",
                customer_id="C-1001",
                status="DELIVERED",
                total_amount=129.90,
            ),
            OrderDB(
                id="NC-1002",
                customer_id="C-1002",
                status="SHIPPED",
                total_amount=4599.00,
            ),
            OrderDB(
                id="NC-1003",
                customer_id="C-1003",
                status="PROCESSING",
                total_amount=89.00,
            ),
        ]

        db.add_all(orders)
        db.commit()

        print("Orders seeded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    seed_orders()