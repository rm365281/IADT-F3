import logging
import os
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_ollama import OllamaEmbeddings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MONGODB_URI = os.environ.get('MONGODB_URI')
OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'llama3')

if not MONGODB_URI:
    logging.warning("MONGODB_URI not set. MongoDBAtlasVectorSearch may fail to connect.")

logging.info("Initializing Ollama Embeddings...")
embeddings = OllamaEmbeddings(model=OLLAMA_MODEL)
logging.info("Ollama Embeddings initialized.")

logging.info("Setting up MongoDB Vector Search...")
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string=MONGODB_URI,
    namespace="hospital_records.patients",
    embedding=embeddings,
    index_name="vector_index"
)
logging.info("MongoDB Vector Search setup complete.")