from typing import List, Literal, TypedDict

from dataclasses import field, dataclass

@dataclass
class UserInputInfo(TypedDict):
    patient: bool = field(default=False)
    """Whether patient data is required."""

    internal_procedures: bool = field(default=False)
    """Whether internal medical procedures are required."""

    disease_info: bool = field(default=False)
    """Whether disease information is required."""

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

@dataclass
class Feedback(TypedDict):
    grade: Literal["Helpful", "Unhelpful"] = field(default="")
    """
    Indicates whether the response was helpful or unhelpful.
    """
    feedback: str = field(
        default=""
    )
    """If the response was unhelpful, provide feedback on how to improve it."""