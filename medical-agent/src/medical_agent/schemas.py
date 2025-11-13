from typing import List, Literal, TypedDict

from dataclasses import field, dataclass

@dataclass
class UserInputInfo(TypedDict):
    """Normalized user input information."""

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

    original_input: str = field(default="")
    """
    The original input text provided by the user.
    This can be used to retain the unprocessed user input for reference.
    """

    summary: str = field(default="")
    """
    A summarized version of the user's input.
    This can be used to condense the information provided by the user for easier analysis.
    """

@dataclass
class RequiredInfo(TypedDict):
    """Flags indicating required information."""

    patient: bool = field(default=True)
    """
    A flag indicating whether additional patient information is required.
    This can be used to determine if the agent needs to ask for more details from the user.
    """

    procedure_guidelines: bool = field(default=False)
    """
    A flag indicating whether medical procedure guidelines are needed.
    This can be used to decide if the agent should reference specific medical protocols or guidelines.
    """

    disease_infos: bool = field(default=False)
    """
    A flag indicating whether additional disease information is required.
    This can be used to determine if the agent needs to gather more details about specific diseases mentioned by the user.
    """