ROBUSTNESS_CASES = [
    {
        "message": "Track order NC-9999",
        "expected_error_contains": "not found",
    },
    {
        "message": "Cancel order NC-1002",
        "expected_error_contains": "cannot be cancelled",
    },
    {
        "message": "Refund order NC-1003",
        "expected_error_contains": "Missing required arguments",
    },
    {
        "message": "Refund RM50 for order NC-1003",
        "expected_error_contains": "already been issued",
    },
    {
        "message": "Cancel order NC-1003",
        "expected_error_contains": "cannot be cancelled",
    },
]