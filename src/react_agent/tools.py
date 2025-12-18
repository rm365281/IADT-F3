"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

import asyncio
import asyncio
import logging

from typing import Any, Callable, List

from langchain.tools import tool
from langgraph.runtime import get_runtime

from react_agent.context import Context
from react_agent.utils import load_openai_model
from react_agent.vector_stores import procedure_vector_store

logger = logging.getLogger(__name__)

@tool
def retrieve_procedure_info(query: str) -> str:
    """
    Tool to retrieve information about hospital procedures based on a query.
    """
    runtime = get_runtime(Context)
    retrieved_docs = procedure_vector_store(runtime).similarity_search_with_score(query, k=1)

    serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc, _ in retrieved_docs
        )

    logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query}")
    logger.info(f"Retrieved documents content: {[doc for doc, _ in retrieved_docs]}")

    return serialized, retrieved_docs[0]

@tool
async def disease_diagnosis(query: str) -> str:
    """
    Tool to assist with disease diagnosis and ask disease-related questions.
    """
    runtime = get_runtime(Context)
    model = await asyncio.to_thread(load_openai_model, runtime.context.medical_model, runtime.context.open_ai_url)
    result = await model.ainvoke({"role": "user", "content": query})
    return result["messages"][-1].content

TOOLS: List[Callable[..., Any]] = [retrieve_procedure_info, disease_diagnosis]