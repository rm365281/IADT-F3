from typing import Literal

from langgraph.graph import END

from react_agent.state import State


def requires_patient_data(state: State) -> bool:
    return state['require_patient_data']

def requires_internal_procedures(state: State) -> bool:
    return state['require_internal_procedures']

def requires_disease_info(state: State) -> bool:
    return state['require_disease_info']

def route_final_answear(state: State) -> Literal[END, "final_answer"]:
    """
    Route to END or evaluator based on evaluation feedback.
    """

    if state['feedback']['grade'] == "Helpful":
        return END
    elif state['feedback']['grade'] == "Unhelpful":
        return "final_answer"