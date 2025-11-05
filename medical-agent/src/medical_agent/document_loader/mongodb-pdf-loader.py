import logging
from vector_store import vector_store
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

class MongoDbPdfLoader:
    """
    A class to load PDF documents to MongoDB.
    """
    def __init__(self):
        self.vector_store = vector_store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20,
            add_start_index=True
        )
        self.vector_store.create_vector_search_index(
            dimensions=1024
        )
        logging.info("MongoDB Vector Search index created.")

    def load(self, file_path: str):
        logging.info("Loading PDF document...")
        docs = PyPDFLoader(file_path).load()
        logging.info("PDF document loaded.")

        logging.info("Splitting document into chunks...")
        all_splits = self.text_splitter.split_documents(docs)
        logging.info("Document split into chunks.")

        logging.info("Adding documents to vector store...")
        document_ids = self.vector_store.add_documents(all_splits)
        logging.info("Documents added to vector store.")

        logging.info(f"Added {len(document_ids)} documents to the vector store with IDs: {document_ids}")