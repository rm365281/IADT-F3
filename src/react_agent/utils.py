"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain.embeddings import init_embeddings
from langchain_openai import ChatOpenAI


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(model, model_provider=provider)

def load_embedding_model(fully_specified_name: str) -> BaseChatModel:
    """Load an embedding model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_embeddings(model, provider=provider)

def load_openai_model(model: str, base_url: str) -> BaseChatModel:
    """Load an OpenAI-compatible model.

    Args:
        model (str): The model name.
        base_url (str): The base URL for the OpenAI-compatible API.
    """

    return ChatOpenAI(base_url=base_url, model=model, api_key="none")