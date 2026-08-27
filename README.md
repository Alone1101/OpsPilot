# OpsPilot

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-blueviolet)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

OpsPilot is an evaluation-driven LLM agent for automating customer operations workflows.

It combines LLM-based intent classification, structured tool execution, retrieval-augmented generation (RAG), policy-aware escalation, and automated evaluation within a LangGraph-orchestrated backend. The system supports both local and hosted LLM inference and exposes selected capabilities through the Model Context Protocol (MCP).

<img width="2553" height="1464" alt="image" src="https://github.com/user-attachments/assets/39cc35b4-bdf0-4dd5-9e64-53a24659ff7e" />

## Overview

Customer-support agents need to do more than generate text. They must distinguish between informational questions and operational requests, retrieve relevant policies, invoke the correct tools, enforce business rules, and escalate actions that should not be performed autonomously.

OpsPilot implements this as a controlled agent workflow:

- Classifies requests as operational actions or policy questions
- Selects and executes structured order-management tools
- Extracts order IDs, refund amounts, and other tool arguments
- Retrieves company policies using vector search
- Enforces deterministic business rules at the service layer
- Escalates operations that exceed autonomous limits
- Supports local LLM inference with Ollama and hosted inference with Gemini
- Exposes read-only order capabilities through MCP
- Evaluates agent decisions, retrieval quality, robustness, and end-to-end workflows

## Architecture

```text
                         ┌──────────────────┐
                         │   Operator UI    │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         │  Agent Workflow  │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
              ┌──────────────┐          ┌──────────────┐
              │    ACTION    │          │    POLICY    │
              │              │          │   QUESTION   │
              └──────┬───────┘          └──────┬───────┘
                     │                         │
                     ▼                         ▼
              ┌──────────────┐          ┌──────────────┐
              │ Tool Registry│          │ RAG Retrieval│
              └──────┬───────┘          └──────┬───────┘
                     │                         │
                     ▼                         ▼
              ┌──────────────┐          ┌──────────────┐
              │Service Layer │          │ Policy Store │
              └──────┬───────┘          └──────┬───────┘
                     │                         │
                     └────────────┬────────────┘
                                  ▼
                         ┌──────────────────┐
                         │ PostgreSQL       │
                         │ + pgvector       │
                         └──────────────────┘
```

LLM decisions can be served locally through Ollama or through Gemini. Deterministic business rules remain outside the LLM and are enforced by the service layer.

## Agent Capabilities

OpsPilot currently supports:

| Tool | Purpose |
| --- | --- |
| `get_order` | Retrieve general order information |
| `get_tracking_status` | Retrieve current shipment status |
| `cancel_order` | Request cancellation of an eligible order |
| `check_refund_eligibility` | Determine whether an order can be refunded |
| `issue_refund` | Process an eligible refund |
| `escalate_case` | Send a case for human review |

Tool arguments are extracted into structured data before execution. Business-rule validation is performed independently of the LLM.

## Policy-Aware RAG

General policy questions are routed through a retrieval pipeline backed by PostgreSQL and pgvector.

The policy knowledge base currently covers:

- Refund policy
- Cancellation policy
- Delivery and order-status policy
- Human escalation policy

Retrieved policy context is supplied to the LLM to generate grounded responses rather than relying solely on model knowledge.

<img width="2530" height="1456" alt="image" src="https://github.com/user-attachments/assets/a23ec809-e35f-4a25-8ffe-e81fa05d3851" />

## Safety and Business Rules

OpsPilot separates probabilistic LLM decisions from deterministic operational constraints.

Examples include:

- Only eligible order states can be cancelled
- Duplicate refunds are rejected
- Refund execution requires an explicit amount
- Refunds above RM250 require human escalation
- Invalid order IDs return controlled domain errors
- Unsafe or unsupported operations can be routed to a human operator

This ensures that selecting a tool does not automatically authorize the requested operation.

<img width="2537" height="1464" alt="image" src="https://github.com/user-attachments/assets/c94c34a8-f545-4a3d-98d3-188974482d5c" />

## Evaluation

OpsPilot includes an automated evaluation harness covering agent decisions, retrieval quality, robustness, and complete workflows.

### Held-Out Agent Evaluation

| Metric | Result |
| --- | ---: |
| Request classification | 15/15 (100%) |
| Tool selection | 14/15 (93.3%) |
| Order ID extraction | 15/15 (100%) |
| Amount extraction | 15/15 (100%) |
| Mean end-to-end latency | 10.76 s |

The remaining tool-selection error involved ambiguity between general order lookup and shipment tracking for the request:

> "I want to know the status of NC-1002"

### RAG Retrieval Evaluation

| Metric | Result |
| --- | ---: |
| Recall@1 | 6/8 (75%) |
| Recall@3 | 8/8 (100%) |
| Mean retrieval latency | 0.50 s |
| Median retrieval latency | 0.48 s |

The results indicate that the expected policy document was retrieved within the top three results for every evaluation query.

### Robustness Evaluation

Robustness tests cover invalid orders, invalid state transitions, missing arguments, duplicate refunds, and repeated cancellation attempts.

**Result: 5/5 cases handled correctly (100%).**

### End-to-End Evaluation

End-to-end scenarios validate complete agent workflows, including:

- Cancellation of an eligible processing order
- Escalation of a high-value refund

Both workflows pass after deterministic business-rule enforcement.

## MCP Interoperability

OpsPilot exposes selected read-only capabilities through a Streamable HTTP Model Context Protocol server.

Validated MCP functionality includes:

- MCP session initialization
- Dynamic tool discovery
- Remote `get_order` invocation
- Remote `get_tracking_status` invocation
- PostgreSQL-backed execution
- Structured MCP responses

This allows external MCP-compatible clients to discover and invoke selected OpsPilot capabilities without directly depending on the application's internal tool registry.

## Operator Dashboard

OpsPilot includes a lightweight web interface served directly by FastAPI.

The dashboard supports:

- Submitting customer requests
- Viewing tool execution results
- Viewing RAG-generated policy answers
- Structured presentation of order information
- Clear success and failure states
- Markdown-rendered policy responses

The dashboard intentionally remains lightweight so that the project focuses on agent architecture and evaluation rather than frontend complexity.

## Technology Stack

**Backend**
- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy

**Agent and LLM**
- LangGraph
- Ollama
- Gemini

**Retrieval**
- PostgreSQL
- pgvector

**Interoperability**
- Model Context Protocol (MCP)

**Infrastructure**
- Docker
- Docker Compose

**Evaluation**
- Held-out agent decision evaluation
- RAG Recall@K evaluation
- Robustness testing
- End-to-end workflow testing
- Latency measurement

## Project Structure

```text
OpsPilot/
├── agents/             # Agent graph and LLM clients
├── evals/              # Evaluation harness and test cases
├── policies/           # Policy knowledge base
├── scripts/            # Utility and MCP test scripts
├── services/           # Business logic and retrieval services
├── static/             # Operator dashboard
├── tools/              # Agent tools and registry
├── database.py
├── exceptions.py
├── main.py
├── mcp_server.py
├── models.py
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Running OpsPilot

### 1. Create the environment

```bash
conda create -n opspilot python=3.12
conda activate opspilot
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file from the provided example configuration and configure the required database and LLM settings.

### 3. Start infrastructure

```bash
docker compose up -d
```

### 4. Start the API

```bash
uvicorn main:app --reload
```

The API documentation is available through `/docs`, and the operator dashboard is available through `/ui/`.

## Running Evaluations

Held-out agent evaluation:

```bash
python -m evals.run_eval test
```

RAG retrieval evaluation:

```bash
python -m evals.run_rag_eval
```

Robustness evaluation:

```bash
python -m evals.run_robustness_eval
```

End-to-end evaluation:

```bash
python -m evals.run_e2e_eval
```

## Design Principles

OpsPilot is built around three principles:

1. **LLMs decide; deterministic services enforce.**  
   The model can classify requests and select tools, but business rules remain in conventional application code.

2. **Agent behaviour should be measured.**  
   Tool selection, argument extraction, retrieval quality, robustness, and workflow outcomes are evaluated explicitly rather than assessed through a few hand-picked demos.

3. **Interoperability should not require rewriting core logic.**  
   FastAPI, the internal agent workflow, and MCP reuse the same underlying service layer.

## Status

OpsPilot is a functional portfolio prototype demonstrating an evaluation-driven approach to building LLM agents for customer operations.
