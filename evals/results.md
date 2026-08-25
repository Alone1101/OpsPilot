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