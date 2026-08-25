RAG_CASES = [
    {
        "query": "What happens if a refund is above RM250?",
        "expected_document": "refund_policy.md",
    },
    {
        "query": "When can an order be cancelled?",
        "expected_document": "cancellation_policy.md",
    },
    {
        "query": "What does SHIPPED mean?",
        "expected_document": "delivery_policy.md",
    },
    {
        "query": "Which cases require a human operator?",
        "expected_document": "escalation_policy.md",
    },
    {
        "query": "Can a cancelled order receive a refund?",
        "expected_document": "refund_policy.md",
    },
    {
        "query": "Can I cancel something that has already shipped?",
        "expected_document": "cancellation_policy.md",
    },
    {
        "query": "What does PROCESSING mean for delivery?",
        "expected_document": "delivery_policy.md",
    },
    {
        "query": "What happens to high-value disputes?",
        "expected_document": "escalation_policy.md",
    },
]