import logging
from typing import Literal

from langgraph.graph import END

from react_agent.state import State

logger = logging.getLogger(__name__)

def in_scope(state: State) -> bool:
    return state.get('in_scope', False)

def requires_patient_data(state: State) -> bool:
    return state['require_patient_data']

def requires_internal_procedures(state: State) -> bool:
    return state['require_internal_procedures']

def requires_disease_info(state: State) -> bool:
    return state['require_disease_info']

def synced(state: State) -> bool:
    is_synced: bool = False

    if state['require_patient_data']:
        patient_details = state.get('patient_data', "")
        is_synced = (patient_details != "")
    if state['require_internal_procedures']:
        internal_procedures_data = state.get('internal_procedures_data', "")
        is_synced = (internal_procedures_data != "")
    if state['require_disease_info']:
        disease_info_data = state.get('disease_info_data', "")
        is_synced = (disease_info_data != "")
    
    logger.info(f"Synced check: {is_synced}")

    return is_synced

    
def route_final_answear(state: State) -> Literal[END, "final_answer"]:
    """
    Route to END or evaluator based on evaluation feedback.
    """

    if state['feedback']['grade'] == "Helpful":
        return END
    elif state['feedback']['grade'] == "Unhelpful":
        return "final_answer"