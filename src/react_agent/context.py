"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated

from . import prompts


@dataclass(kw_only=True)
class Context:
    """The context for the agent."""

    system_prompt: str = field(
        default=prompts.USER_INPUT_NORMALIZATION_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    final_answer_prompt: str = field(
        default=prompts.FINAL_ANSWER_PROMPT,
        metadata={
            "description": "The prompt to use when the agent is generating the final answer. "
            "This prompt guides the agent to summarize and conclude the interaction."
        },
    )

    patient_info_query_prompt: str = field(
        default=prompts.PATIENT_INFO_QUERY_PROMPT,
        metadata={
            "description": "The prompt to use when querying patient information. "
            "This prompt helps the agent to formulate queries for retrieving patient data."
        },
    )

    procedure_info_query_prompt: str = field(
        default=prompts.PROCEDURE_INFORMATION_PROMPT,
        metadata={
            "description": "The prompt to use when querying internal medical procedure information. "
            "This prompt helps the agent to formulate queries for retrieving procedure data."
        },
    )

    disease_diagnosis_prompt: str = field(
        default=prompts.DISEASE_DIAGNOSIS_PROMPT,
        metadata={
            "description": "The prompt to use when querying disease diagnosis information. "
            "This prompt helps the agent to formulate responses related to disease diagnoses."
        },
    )

    evaluation_prompt: str = field(
        default=prompts.EVALUATION_PROMPT,
        metadata={
            "description": "The prompt to use when evaluating model responses. "
            "This prompt guides the agent to assess the quality and relevance of responses."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="ollama/llama3.1:8b",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    medical_model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="Groff/tech3_model.gguf",
        metadata={
            "description": "The name of the language model to use for medical-specific interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    embedding_model: Annotated[str, {"__template_metadata__": {"kind": "embedding"}}] = field(
        default="ollama/llama3",
        metadata={
            "description": "The name of the embedding model to use for vector store operations. "
            "Should be in the form: provider/model-name."
        },
    )

    mongodb_connection_string: str = field(
        default=os.environ.get('MONGODB_URI'),
        metadata={
            "description": "The MongoDB connection string for the vector store."
        },
    )

    mongodb_namespace: str = field(
        default="hospital_records.procedures",
        metadata={
            "description": "The MongoDB namespace (database.collection) for the vector store."
        },
    )

    open_ai_url: str = field(
        default="http://192.168.0.15:1234/v1",
        metadata={
            "description": "The base URL for the OpenAI-compatible API."
        },
    )

    def __post_init__(self) -> None:
        """Fetch env vars for attributes that were not passed as args."""
        for f in fields(self):
            if not f.init:
                continue

            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))