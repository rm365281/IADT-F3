from typing import Any

from langchain.agents.middleware import AgentMiddleware, hook_config
from langchain.agents.middleware.types import StateT
from langgraph.runtime import Runtime

from typing import Any
import re
import logging

from langchain.agents.middleware import AgentMiddleware, hook_config
from langchain.agents.middleware.types import StateT

logger = logging.getLogger(__name__)


class DatabaseWriteOperationGuardrail(AgentMiddleware):
    """
    A guardrail that prevents write operations to the database.

    Behavior:
    - Scans incoming human/user messages for SQL write operation keywords.
    - Uses word-boundary regex checks to reduce accidental matches.
    - Returns an assistant message and jumps to "end" when a write intent is detected.
    """

    def __init__(self):
        super().__init__()
        self.write_operations = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE"]
        pattern = r"\b(" + "|".join(self.write_operations) + r")\b"
        self._write_regex = re.compile(pattern, flags=re.IGNORECASE)

    @hook_config(can_jump_to=["end"])
    def before_agent(self, state: StateT) -> dict[str, Any] | None:
        """Inspect messages and block any that appear to request DB write operations.

        The middleware is defensive about message shapes: it accepts message objects
        that expose `.type`, `.role`, `.content`, or `.text`. Only messages that are
        human/user-initiated are inspected.
        """
        try:
            messages = state.get("messages") or []
        except Exception:
            logger.debug("State has no messages or is malformed")
            return None

        for msg in messages:
            # Determine if this is a human/user message. Accept multiple shapes.
            msg_type = getattr(msg, "type", None) or getattr(msg, "role", None) or None
            if msg_type and str(msg_type).lower() not in ("human", "user"):
                continue

            # Extract text content from common attributes
            content = None
            for attr in ("content", "text", "message", "body"):
                content = getattr(msg, attr, None)
                if content:
                    break

            if not content:
                # If msg is a plain dict-like mapping
                try:
                    content = msg.get("content") or msg.get("text")
                except Exception:
                    content = None

            if not content:
                continue

            # Run the regex to detect write operation keywords
            try:
                if self._write_regex.search(str(content)):
                    logger.info("Blocked potential DB write operation detected in user message")
                    return {
                        "messages": [
                            {
                                "role": "assistant",
                                "content": (
                                    "Database write operations are not permitted. "
                                    "If you need data modified, please rephrase to request a read-only query "
                                    "or escalate to a human operator who can perform database changes."
                                ),
                            }
                        ],
                        "jump_to": "end",
                    }
            except Exception:
                logger.exception("Error while scanning message content for write operations")

        return None