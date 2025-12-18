# Medical AI Assistant

This project is a Medical AI Assistant designed to provide comprehensive responses to user queries by integrating information from multiple sources:

- **Internal Medical Procedures:** Stored in a vector database (MongoDB Atlas).
- **Patient Data:** Stored in a SQL database (MySQL).
- **Disease Information:** Provided by a fine-tuned LLM (based on llama-3.2-3b-instruct-unsloth-bnb-4bit).

The agent can:
- Answer questions about internal medical procedures.
- Retrieve and utilize patient data.
- Provide disease-related information.
- Combine information from all sources to answer complex user requests within its capabilities.

## Architecture

- **Orchestrator-Worker Pattern:** The agent orchestrates and routes requests to the appropriate data sources and models.
- **LangGraph:** Used for building the agent's workflow and orchestration logic.
- **Ollama:** For LLM inference and management.
- **Docker Compose:** For containerized deployment and service management.

## Data Sources

- **Vector Database:** MongoDB Atlas for storing and retrieving medical procedure information using vector search.
- **SQL Database:** MySQL for structured patient data.
- **LLM:** Fine-tuned llama-3.2-3b-instruct-unsloth-bnb-4bit model for disease information and natural language understanding.

## Capabilities

- Intelligent routing and orchestration of user requests.
- Multi-source data integration for comprehensive answers.
- Secure handling of patient and medical data.

## Getting Started

1. **Clone the repository**
2. **Configure environment variables** for database and LLM access.
3. **Start services** using Docker Compose.
4. **Interact with the agent** via the provided API or interface.

## Requirements
- Docker & Docker Compose
- Access to MongoDB Atlas and MySQL
- Ollama for LLM management

## License

See LICENSE for details.
