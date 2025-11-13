from typing import Any, Callable, List
from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.runtime import get_runtime

from context import Context

def procedure_vector_store() -> MongoDBAtlasVectorSearch:
    runtime = get_runtime(Context)
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=runtime.context.mongodb_connection_string,
        namespace=runtime.context.mongodb_namespace,
        embedding=runtime.context.embedding_model,
        index_name="vector_index"
    )
    return vector_store

VECTOR_STORES: List[Callable[..., Any]] = [procedure_vector_store]