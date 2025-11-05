# Medical Agent

## Purpose

This repository implements a modular medical assistant intended to help clinicians by retrieving and explaining relevant hospital information during medical consultations. The assistant is trained/augmented with the hospital's internal protocols and data so it can answer clinical questions and suggest procedures aligned with those protocols.

Key goals:
- Assist clinicians by surfacing protocol-relevant procedures and patient-contextual answers.
- Provide explainability: always state the information source(s) used to form an answer.
- Enforce safety/business rules (e.g., never autonomously prescribe medication without human validation).

> Note: The user provided the phrase "fine-tuned model with ill information"; here we assume this means a model fine-tuned on the hospital's internal (in-house) information. If the original meaning differs, update this README accordingly.

## Scope & Safety (business requirements)

- Define the assistant's scope of action to avoid unsafe or inappropriate suggestions.
	- Never issue prescriptions or definitive treatment plans without explicit human review and sign-off.
	- Flag uncertain answers and require clinician verification for high-risk recommendations.
- Provide explainability for every answer:
	- Cite the source documents, procedures, or database records (e.g., protocol document name, database table, or PDF page) used to generate the answer.
- Maintain patient-contextual answers:
	- Query and incorporate up-to-date patient-specific data from the structured database (MySQL) during interactions.
- Support structured database queries:
	- Allow the `sql-agent` to run controlled, audited queries against MySQL (patient history) and return structured results.

## Non-functional requirements

- Logging and auditing: all queries, agent actions, and final outputs must be logged for traceability and post-hoc review.
- Modularity: the codebase is structured so individual agents (SQL, PDF, supervisor, vector store) are separable and testable.
- Performance: keep response times reasonable for interactive clinical use — use vector stores and targeted retrieval to avoid unnecessary LLM calls.

## Stack

- Language: Python
- LLM / embeddings: GPT-OSS:20b (LLM), llama3 (embeddings) — used as indicated by project configuration
- Libraries: LangChain (agent orchestration), plus DB connectors
- Data stores:
	- MongoDB: used as a vector database to store medical procedure information (embeddings + metadata)
	- MySQL: stores patient health history and structured clinical data

## Models and Agents

- LLM Model(s):
	- GPT-OSS:20b — used as the primary text-generation model.
	- Note: the project references a fine-tuned model trained on hospital data (see caveat above).
- Embeddings: llama3 (for producing vector embeddings stored in MongoDB).

- Agents involved:
	- `sql-agent` — retrieves patient information from MySQL (`src/medical_agent/agents/sql-agent.py`).
	- `pdf-agent` — retrieves and indexes hospital internal procedures from PDFs and other documents (`src/medical_agent/agents/pdf-agent.py`).
	- `supervisor` (supervisor model) — coordinates the other agents and composes the final, human-reviewable answer.

Refer to the `src/medical_agent/agents/` folder for agent implementations. (Files present in this repo: `pdf-agent.py`, `sql-agent.py`, and a `custom_guardrail` helper.)

## Data flows / Architecture (brief)

1. Document ingestion: hospital procedure documents (PDFs) are processed by the `pdf-agent` and indexed in MongoDB as vectors with metadata.
2. Patient context: the `sql-agent` queries MySQL for the patient's up-to-date medical history and relevant structured fields.
3. Retrieval: when a clinician asks a question, the supervisor
	 - sends retrieval requests to the vector store (MongoDB) to find relevant procedures and citations,
	 - queries MySQL for the patient's data,
	 - composes prompts using both retrieved textual evidence and structured patient data,
	 - calls the LLM to produce an explainable, source-cited recommendation which is then returned to the clinician for validation.

## Logging & Auditing

- Log entries should include: timestamp, agent(s) invoked, DB queries executed (parameterized), documents retrieved (IDs/pages), LLM prompts & model used, and final output (tagged as "requires human validation" where applicable).
- Keep logs in a secure, access-controlled store (not checked into this repo).

## Security, Privacy & Compliance

- Patient data is sensitive. This project must ensure that:
	- All access to MySQL and MongoDB is over secure channels and access-controlled.
	- No PHI (protected health information) is exposed in logs unless logs are secured and access audited.
	- Human-in-the-loop approval is required before any actionable clinical recommendation is treated as a final order.

## Project layout (key files)

- `pyproject.toml` — project metadata and dependencies
- `compose.yaml` — docker-compose (if present) for services
- `db/` — SQL schema and seed data (`1_schema.sql`, `2_users.sql`, `3_data.sql`)
- `src/medical_agent/` — core source code
	- `vector_store.py` — vector store helpers
	- `agents/pdf-agent.py` — PDF retrieval / ingestion
	- `agents/sql-agent.py` — SQL query agent
	- `agents/custom_guardrail/` — guardrail/constraints for agents
	- `document_loader/mongodb-pdf-loader.py` — example loader for PDFs into MongoDB

When referencing these files in issues or PRs, use backticks (e.g., `src/medical_agent/agents/pdf-agent.py`).

## How to run (developer quickstart)

1. Create a Python environment (3.10+ recommended) and install dependencies from `pyproject.toml`.
2. Configure environment variables / secrets for:
	 - MySQL connection (host, port, user, password, database)
	 - MongoDB connection string
	 - LLM endpoints / API keys for GPT-OSS:20b and llama3 embeddings (if required)
3. Seed the MySQL DB using `db/1_schema.sql`, `db/2_users.sql`, `db/3_data.sql` (only in a safe test environment).
4. Run ingestion for hospital PDFs using the loader to populate the MongoDB vector store.
5. Start the agent supervisor or run the example scripts in `src/medical_agent/agents/`.

Example commands (developer machine):

```bash
# create venv
python -m venv .venv
source .venv/bin/activate
pip install -e .

# (configure env vars) then run a simple script or the supervisor
python -m src.medical_agent.agents.pdf-agent
```

Adjust the module path and run commands to match your development layout.

## Notes & next steps

- Enforce the human-in-the-loop requirement in code paths that produce treatment recommendations. The supervisor should mark high-risk outputs and include an explicit clinician confirmation step.
- Add unit/integration tests for the `sql-agent` (DB query layer) and `pdf-agent` (document retrieval and citation accuracy).
- Implement structured logging and configurable log sinks (file, central logging service) with RBAC.

## Contribution & license

- Contributions: open a PR against this repo. Document any data-handling changes in PR descriptions.
- License: (add license information here)

## Contact

For questions about this repo or model/data usage, contact the project owner or hospital data governance team.

