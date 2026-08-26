E2E_CASES = [
    {
        "name": "cancel_processing_order",
        "message": "Cancel order NC-1003",
        "expected_tool": "cancel_order",
        "expected_order_status": "CANCELLED",
    },
    {
        "name": "high_value_refund_escalation",
        "message": "Refund RM400 for order NC-1002",
        "expected_tool": "escalate_case",
        "expected_escalation_status": "PENDING",
    },
]