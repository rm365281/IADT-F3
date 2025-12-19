"""Define the state structures for the agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing_extensions import Annotated

from react_agent.schemas import Feedback

@dataclass
class InputState(TypedDict):
    """Defines the input state for the agent, representing a narrower interface to the outside world.

    This class is used to define the initial state and structure of incoming data.
    """

    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    """
    Messages tracking the primary execution state of the agent.

    Typically accumulates a pattern of:
    1. HumanMessage - user input
    2. AIMessage with .tool_calls - agent picking tool(s) to use to collect information
    3. ToolMessage(s) - the responses (or errors) from the executed tools
    4. AIMessage without .tool_calls - agent responding in unstructured format to the user
    5. HumanMessage - user responds with the next conversational turn

    Steps 2-5 may repeat as needed.

    The `add_messages` annotation ensures that new messages are merged with existing ones,
    updating by ID to maintain an "append-only" state unless a message with the same ID is provided.
    """


@dataclass
class State(InputState):
    require_patient_data: bool = field(default=False)
    """Flag indicating if patient data is required."""
    patient_data: str = field(default="")
    """Holds patient data requirements and details."""


    require_internal_procedures: bool = field(default=False)
    """Flag indicating if internal medical procedures are required."""
    internal_procedures_data: str = field(default="")
    """Holds internal medical procedures requirements and details."""


    require_disease_info: bool = field(default=False)
    """Flag indicating if disease information is required."""
    disease_info_data: str = field(default="")
    """Holds disease information requirements and details."""

    patient_name: str = field(default="")
    """
    The name of the patient provided by the user.
    This can be used to identify the patient in subsequent interactions.
    """

    symptoms: List[str] = field(default_factory=list)
    """
    A list of symptoms provided by the user.
    This can be used to track the symptoms reported during the interaction.
    """

    disease_name: str = field(default="")
    """
    The name of the disease mentioned by the user.
    This can be used to identify specific diseases referenced in the conversation.
    """

    condition: str = field(default="")
    """
    The overall condition described by the user.
    This can be used to summarize the user's health status.
    """

    medical_procedure: str = field(default="")
    """
    The internal medical procedure requested by the user.
    This can be used to identify specific procedures mentioned during the interaction.
    """

    combined_output: str = field(default="")
    """Holds the final aggregated output for the user."""

    feedback: Feedback = field(default_factory=Feedback)
    """
    Feedback on the agent's responses.
    This can be used to evaluate the quality of the agent's advice and improve future interactions.
    """

    in_scope: bool = field(default=True)
    """Indicates whether the user query is within the agent's scope."""