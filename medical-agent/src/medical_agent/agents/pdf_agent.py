import logging

from langchain.agents import create_agent
from vector_stores import vector_store
from langchain_ollama import ChatOllama
from langchain.agents.middleware import dynamic_prompt, ModelRequest


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__model = ChatOllama(model="gpt-oss:20b")

retriever = vector_store.as_retriever(search_kwargs={"k": 3})


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject retrieval results and a stronger system prompt into state messages.

    This middleware will (1) retrieve the most relevant hospital procedures for the
    user's last query, (2) provide those documents as context to the model, and
    (3) include explicit guardrails: require citation of sources, avoid
    autonomous prescribing, and present any recommendation as requiring human
    validation.
    """
    last_query = request.state["messages"][-1].text
    logger.info("Received user query for PDF retrieval: %s", last_query)

    try:
        logger.info("Attempting retrieval using retriever.get_relevant_documents")
        retrieved_docs = retriever.get_relevant_documents(last_query)
    except Exception:
        logger.exception("Retriever.get_relevant_documents() failed, falling back to vector_store.similarity_search()")
        retrieved_docs = vector_store.similarity_search(last_query)

    logger.info("Retrieved %d document(s) from vector store", len(retrieved_docs))

    def fmt_doc(doc):
        meta = doc.metadata or {}
        source = meta.get("source") or meta.get("filename") or meta.get("title") or meta.get("file_name") or meta.get("document_id") or "unknown-source"
        page = meta.get("page") or meta.get("page_number") or "unknown-page"
        header = f"---\nSource: {source} | Page: {page}\n---"
        return f"{header}\n{doc.page_content}\n"

    docs_content = "\n".join(fmt_doc(doc) for doc in retrieved_docs)

    # Log the list of retrieved sources (non-sensitive metadata only)
    try:
        sources = [
            f"{(doc.metadata or {}).get('source') or (doc.metadata or {}).get('filename') or 'unknown-source'}:"
            f"{(doc.metadata or {}).get('page') or (doc.metadata or {}).get('page_number') or 'unknown-page'}"
            for doc in retrieved_docs
        ]
        logger.info("Retrieval sources: %s", ", ".join(sources) if sources else "none")
    except Exception:
        logger.debug("Failed to build sources list for logging")

    system_message = (
        "You are a clinical assistant specialized in hospital procedures. Follow these steps before answering:\n"
        "1) Carefully read the user query (shown below).\n"
        "2) From the retrieved procedure documents provided, identify the most relevant hospital procedure(s) that address the query.\n"
        "3) For each matching procedure, give a one-line rationale for relevance and cite the source using the document filename and page number.\n"
        "4) Provide a concise, protocol-aligned recommendation phrased as guidance for a clinician (NOT as a final prescription or order). Always require human validation for any treatment or medication recommendation.\n"
        "5) If patient-specific structured data is available in the conversation state, call it out and explain how it affected the recommendation.\n"
        "6) If no relevant procedure is found, explicitly state that and suggest safe next steps (e.g., consult specialist, obtain missing data).\n"
        "7) Include a short 'Confidence' statement and a 'Sources' section listing the document filenames and page numbers used.\n\n"
        "IMPORTANT: Do not hallucinate procedures or sources. Use only the text and metadata from the retrieved documents. If uncertain, say so and do not invent treatments.\n\n"
        "User query:\n" + last_query + "\n\n"
        "Retrieved procedure documents (most relevant first):\n\n" + docs_content
    )

    try:
        logger.debug("Built system message (chars): %d", len(system_message))
    except Exception:
        logger.debug("Could not compute system_message length")

    return system_message


agent = create_agent(__model, tools=[], middleware=[prompt_with_context])