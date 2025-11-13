from dataclasses import dataclass, field
from typing import List, List, Literal, Sequence, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing_extensions import Annotated
from langchain_core.documents import Document

from medical_agent.schemas import RequiredInfo, UserInputInfo


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
class MedicalState(InputState):
    """Represents the complete state of the medical agent.
    
    This class can be used to store any information needed throughout the agent's lifecycle.
    """

    patient_info: List[Document] = field(default_factory=list)
    """
    A list of documents retrieved during the agent's operation.
    This can be used to store information fetched from external sources, such as medical databases or knowledge bases.
    """

    procedure_guidelines : List[Document] = field(default_factory=list)
    """
    A list of medical procedure guidelines relevant to the patient's condition.
    This can be used to reference standard protocols and best practices during diagnosis and treatment planning.
    """

    possible_diagnoses: List[str] = field(default_factory=list)
    """
    A list of possible diagnoses based on the symptoms and information gathered.
    This can be used to store potential medical conditions identified by the agent.
    """

    recommended_tests: List[str] = field(default_factory=list)
    """
    A list of recommended medical tests for further diagnosis.
    """

    treatment_options: List[str] = field(default_factory=list)
    """
    A list of treatment options suggested by the agent.
    """

    follow_up_questions: List[str] = field(default_factory=list)
    """
    A list of follow-up questions to ask the user for more information.
    """

    referrals: List[str] = field(default_factory=list)
    """
    A list of referrals to specialists or medical professionals.
    """

    patient_health_history: List[str] = field(default_factory=list)
    """
    A list of relevant patient health history details.
    """

    user_input_info: UserInputInfo = field(default_factory=UserInputInfo)
    """
    Normalized information extracted from user input.
    This can be used to structure and analyze the user's symptoms, disease names, and overall condition.
    """

    required_info: RequiredInfo = field(default_factory=RequiredInfo)
    """
    Flags indicating what additional information is required.
    This can be used to determine if the agent needs to gather more details about the patient, procedure guidelines, or disease information.
    """