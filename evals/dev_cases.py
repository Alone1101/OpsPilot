DEV_CASES = [
    # --- Tracking ---
    {
        "message": "Track order NC-1002",
        "expected_request_type": "ACTION",
        "expected_tool": "get_tracking_status",
        "expected_order_id": "NC-1002",
    },
    {
        "message": "Where is my order NC-1002?",
        "expected_request_type": "ACTION",
        "expected_tool": "get_tracking_status",
        "expected_order_id": "NC-1002",
    },
    {
        "message": "Has NC-1002 shipped yet?",
        "expected_request_type": "ACTION",
        "expected_tool": "get_tracking_status",
        "expected_order_id": "NC-1002",
    },
    {
        "message": "What's happening with NC-1002?",
        "expected_request_type": "ACTION",
        "expected_tool": "get_tracking_status",
        "expected_order_id": "NC-1002",
    },

    # --- Cancellation ---
    {
        "message": "Cancel order NC-1003",
        "expected_request_type": "ACTION",
        "expected_tool": "cancel_order",
        "expected_order_id": "NC-1003",
    },
    {
        "message": "Please cancel NC-1003",
        "expected_request_type": "ACTION",
        "expected_tool": "cancel_order",
        "expected_order_id": "NC-1003",
    },
    {
        "message": "Stop NC-1003 before it ships",
        "expected_request_type": "ACTION",
        "expected_tool": "cancel_order",
        "expected_order_id": "NC-1003",
    },

    # --- Refund eligibility ---
    {
        "message": "Can I get a refund for order NC-1003?",
        "expected_request_type": "ACTION",
        "expected_tool": "check_refund_eligibility",
        "expected_order_id": "NC-1003",
    },
    {
        "message": "Check whether NC-1003 is eligible for a refund",
        "expected_request_type": "ACTION",
        "expected_tool": "check_refund_eligibility",
        "expected_order_id": "NC-1003",
    },

    # --- Refund execution ---
    {
        "message": "Refund RM50 for order NC-1003",
        "expected_request_type": "ACTION",
        "expected_tool": "issue_refund",
        "expected_order_id": "NC-1003",
        "expected_amount": 50.0,
    },
    {
        "message": "Give me RM75 back for NC-1003",
        "expected_request_type": "ACTION",
        "expected_tool": "issue_refund",
        "expected_order_id": "NC-1003",
        "expected_amount": 75.0,
    },
    {
        "message": "Refund 100 ringgit on NC-1003",
        "expected_request_type": "ACTION",
        "expected_tool": "issue_refund",
        "expected_order_id": "NC-1003",
        "expected_amount": 100.0,
    },

    # --- Escalation ---
    {
        "message": "Escalate order NC-1002 for human review",
        "expected_request_type": "ACTION",
        "expected_tool": "escalate_case",
        "expected_order_id": "NC-1002",
    },
    {
        "message": "Send NC-1002 to a human operator",
        "expected_request_type": "ACTION",
        "expected_tool": "escalate_case",
        "expected_order_id": "NC-1002",
    },

    # --- Policy questions ---
    {
        "message": "What is your refund policy?",
        "expected_request_type": "POLICY_QUESTION",
        "expected_tool": None,
        "expected_order_id": None,
    },
    {
        "message": "What is the refund policy for RM400?",
        "expected_request_type": "POLICY_QUESTION",
        "expected_tool": None,
        "expected_order_id": None,
    },
    {
        "message": "When can an order be cancelled?",
        "expected_request_type": "POLICY_QUESTION",
        "expected_tool": None,
        "expected_order_id": None,
    },
    {
        "message": "Do refunds above RM250 require human review?",
        "expected_request_type": "POLICY_QUESTION",
        "expected_tool": None,
        "expected_order_id": None,
    },
]