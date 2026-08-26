# OpsPilot Evaluation Results

## Model
- Provider: Ollama
- Model: Qwen3 8B
- Inference: Local
- Temperature: 0

## Agent Decision Evaluation

### Development Set
Cases: 18

| Metric | Result |
|---|---:|
| Request classification accuracy | 18/18 (100.0%) |
| Tool selection accuracy | 18/18 (100.0%) |
| Order ID extraction accuracy | 18/18 (100.0%) |
| Amount extraction accuracy | 18/18 (100.0%) |

The development set was used during prompt refinement and therefore should not be treated as an unbiased final evaluation.

### Held-Out Test Set — Local Qwen3 8B
Cases: 15

| Metric | Result |
|---|---:|
| Request classification accuracy | 15/15 (100.0%) |
| Tool selection accuracy | 14/15 (93.3%) |
| Order ID extraction accuracy | 15/15 (100.0%) |
| Amount extraction accuracy | 15/15 (100.0%) |
| Mean end-to-end latency | 10.72 s |
| Median latency | 9.94s |

### Observed Failure

Input:
"I want to know the status of NC-1002"

Expected tool:
get_tracking_status

Predicted tool:
get_order

The request was correctly classified as ACTION and the order ID was correctly extracted. The error was limited to tool selection between two semantically related order-information tools.

### Observed Outlier

Input: 
"I want to know the status of NC-1002"

Expected tool:
get_tracking_status

Predicted tool:
get_order

Latency: 
22.08 s

## Pre-Tuning Development Baseline

Before prompt refinement:

| Metric | Result |
|---|---:|
| Request classification accuracy | 16/18 (88.9%) |
| Tool selection accuracy | 15/18 (83.3%) |
| Order ID extraction accuracy | 16/18 (88.9%) |
| Amount extraction accuracy | 18/18 (100.0%) |

After prompt refinement, development-set performance reached 100% on all four metrics. Generalization was subsequently evaluated using the separate 15-case held-out set above.

## RAG Retrieval Evaluation
Cases: 8

| Metric | Result |
|---|---:|
| Recall@1 | 6/8 (75.0%) |
| Recall@3 | 8/8 (100.0%) |
| Mean retrieval latency | 0.50 s |
| Median retrieval latency | 0.48 s |

### Observed Retrieval Ambiguities

1. Query:
   "What happens if a refund is above RM250?"

   Expected:
   refund_policy.md

   Top result:
   escalation_policy.md

   The retrieved result is semantically relevant because refunds above RM250 require human escalation.

2. Query:
   "Can a cancelled order receive a refund?"

   Expected:
   refund_policy.md

   Top result:
   cancellation_policy.md

   The query overlaps cancellation and refund policy concepts. The expected refund policy still appeared within the top 3 results.

## Robustness Evaluation
Cases: 5

| Scenario | Result |
|---|---:|
| Nonexistent order | Passed |
| Invalid cancellation state | Passed |
| Missing refund amount | Passed |
| Duplicate refund | Passed |
| Re-cancelling cancelled order | Passed |

Overall robustness handling: **5/5 (100.0%)**

## End-to-End Workflow Evaluation
Cases: 2

| Workflow | Expected Outcome | Result |
|---|---|---:|
| Processing-order cancellation | Order status transitions to `CANCELLED` | Passed |
| High-value refund escalation | Refund above RM250 routes to `escalate_case` and creates a `PENDING` escalation | Passed |

Overall end-to-end workflow success: **2/2 (100.0%)**

### High-Value Refund Escalation

The initial end-to-end evaluation exposed an orchestration issue in which a refund above the RM250 autonomous limit selected `issue_refund` but did not transition through the LangGraph escalation path.

The workflow was revised so that the refund service signals that human review is required, allowing LangGraph to route execution to `escalate_case`.

The resulting workflow is:

`issue_refund` → escalation required → LangGraph conditional routing → `escalate_case` → `PENDING` human-review case

After the fix, both evaluated end-to-end workflows passed.