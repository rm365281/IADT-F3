from langchain_mongodb import MongoDBAtlasVectorSearch
from langgraph.runtime import Runtime

from react_agent.context import Context
from react_agent.utils import load_embedding_model

def procedure_vector_store(runtime: Runtime[Context]) -> MongoDBAtlasVectorSearch:
    embedding_model = load_embedding_model(runtime.context.embedding_model)
    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string=runtime.context.mongodb_connection_string,
        namespace=runtime.context.mongodb_namespace,
        embedding=embedding_model,
        index_name="vector_index"
    )
    return vector_store