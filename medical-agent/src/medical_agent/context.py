"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated
from langchain_community.utilities import SQLDatabase
from . import prompts


@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    planning_prompt: str = field(
        default=prompts.PLANNING_PROMPT,
        metadata={
            "description": "The prompt template to use for the agent's planning step. "
            "This prompt guides the agent in determining the next actions to take."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="ollama/gpt-oss:20b",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    sql_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="ollama/gpt-oss:20b",
        metadata={
            "description": "The name of the language model to use for SQL database interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    #sql_db_connection: SQLDatabase = field(
   #     default=SQLDatabase.from_uri(
   #         database_uri=os.environ.get('DATABASE_URI', 'sqlite:///medical_agent.db')
   #     ),
   #     metadata={
   #         "description": "The database connection for the agent to use for SQL operations."
   #     },
   # )

    mongodb_connection_string: str = field(
        default=os.environ.get('MONGODB_URI'),
        metadata={
            "description": "The MongoDB connection string for the vector store."
        },
    )

    mongodb_namespace: str = field(
        default="hospital_records.patients",
        metadata={
            "description": "The MongoDB namespace (database.collection) for the vector store."
        },
    )

    embedding_model: Annotated[str, {"__template_metadata__": {"kind": "embedding"}}] = field(
        default="ollama/llama3",
        metadata={
            "description": "The name of the embedding model to use for vector store operations. "
            "Should be in the form: provider/model-name."
        },
    )

    retriever_k: int = field(
        default=5,
        metadata={
            "description": "The number of top documents to retrieve from the vector store."
        },
    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        for f in fields(self):
            if not f.init:
                continue

            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))
