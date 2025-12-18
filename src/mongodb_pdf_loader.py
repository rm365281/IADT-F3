import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from react_agent.utils import load_embedding_model

def _is_header_only(text: str) -> bool:
    text = text.strip()
    return len(text) < 80 and text[0].isdigit() and "." in text

embedding_model = load_embedding_model("ollama/llama3")
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=os.environ.get('MONGODB_URI'),
    namespace='hospital_records.procedures',
    embedding=embedding_model,
    index_name="vector_index",
    relevance_score_fn="cosine"
)

vector_store.create_vector_search_index(dimensions=4096)

docs = PyPDFLoader('/home/groff/projects/python/fiap/medical-agent/db/medic-procedures/BasicProcedure.pdf').load()

docs = [
    d for d in docs
    if d.metadata.get("page", 0) > 5
]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1200,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". "],
    add_start_index=True
)

splits = text_splitter.split_documents(docs)

splits = [
    s for s in splits
    if not _is_header_only(s.page_content)
]

vector_store.add_documents(splits)