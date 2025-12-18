# Copilot Instructions for Medical AI Assistant

## Project Overview
- This is a medical AI assistant that answers queries by integrating:
  - Medical procedure info (MongoDB Atlas, vector search)
  - Patient data (MySQL)
  - Disease info (fine-tuned LLM: llama-3.2-3b-instruct-unsloth-bnb-4bit)
- Uses the Orchestrator-Worker pattern for request routing and data orchestration
- Built with LangGraph (workflow/orchestration), Ollama (LLM), and Docker Compose (deployment)

## Key Components
- `src/react_agent/graph.py`: Main orchestration logic, defines the agent's workflow
- `src/react_agent/nodes.py`: Worker nodes for handling specific tasks (e.g., DB queries, LLM calls)
- `src/react_agent/context.py`, `state.py`, `schemas.py`: Shared state, data models, and context passing
- `src/react_agent/vector_stores.py`: Vector DB (MongoDB Atlas) integration for medical procedures
- `src/react_agent/tools.py`, `utils.py`: Utility functions and tool abstractions
- `tests/`: Unit and integration tests (see `tests/integration_tests/test_graph.py` for end-to-end flows)

## Data Flow
- User requests are received by the orchestrator (graph)
- The orchestrator routes sub-tasks to worker nodes:
  - Vector DB for procedures
  - SQL DB for patient data
  - LLM for disease info
- Results are merged and returned to the user

## Developer Workflows
- **Build/Run:** Use `docker compose up` to start all services (Ollama, DBs, agent)
- **Testing:** Run `pytest` from the project root; integration tests use cassettes for reproducibility
- **Environment:** Configure DB/LLM credentials via environment variables (see README)

## Project Conventions
- Follows orchestrator-worker separation: orchestration logic in `graph.py`, workers in `nodes.py`
- Data models and state are centralized in `schemas.py` and `state.py`
- All external integrations (DBs, LLM) are abstracted in dedicated modules
- Use LangGraph for all workflow logic; avoid ad-hoc orchestration

## Integration Points
- MongoDB Atlas (vector search): see `vector_stores.py`
- MySQL (patient data): see `nodes.py` and related DB access code
- Ollama (LLM): see LLM-related nodes and configuration

## Examples
- To add a new data source, create a new worker node in `nodes.py` and update the graph in `graph.py`
- To test a new workflow, add a test in `tests/integration_tests/`

For more details, see the README.md and source files referenced above.
