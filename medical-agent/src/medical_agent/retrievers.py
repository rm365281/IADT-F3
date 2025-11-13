from typing import Any, Callable, List
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langgraph.runtime import get_runtime
from medical_agent.context import Context

def procedure_retriever(vector_store: VectorStore) -> VectorStoreRetriever:
    runtime = get_runtime(Context)
    return vector_store.as_retriever(search_kwargs={"k": runtime.context.retriever_k})

RETRIEVERS: List[Callable[..., Any]] = [procedure_retriever]