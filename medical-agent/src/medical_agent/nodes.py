from re import A
from typing import Dict
from langgraph.runtime import Runtime

from medical_agent.prompts import NORMALIZATION_PROMPT, PLANNING_PROMPT
from medical_agent.schemas import RequiredInfo, UserInputInfo
from medical_agent.state import MedicalState
from medical_agent.utils import load_chat_model
from numpy import require


async def normalize_user_input(state: MedicalState, runtime: Runtime) -> Dict[str, UserInputInfo]:
    """
    Normalize and preprocess user input in the medical state.

    This function can be used to clean or structure the user input messages
    before passing them to the model.

    Args:
        state (MedicalState): The current state of the conversation.
        runtime (Runtime): The runtime context.

    Returns:
        MedicalState: The updated state with normalized user input.
    """

    model = load_chat_model(runtime.context.model)
    structured_model = model.with_structured_output(UserInputInfo)
    user_info_input = await structured_model.ainvoke(
        [{"role": "system", "content": NORMALIZATION_PROMPT}, *state['messages']]
    )

    return {"user_input_info": user_info_input}


async def planning(state: MedicalState, runtime: Runtime) -> Dict[str, RequiredInfo]:
    """
    Define a planning step to generate the next steps in the medical workflow.

    This function uses a chat model to analyze the current state messages
    and produce a list of AI messages that outline the next steps.

    Args:
        state (MedicalState): The current state of the conversation.
        runtime (Runtime): The runtime context.

    Returns:
        Dict[str, RequiredInfo]: A dictionary containing flags indicating required information.
    """

    required_info: RequiredInfo = RequiredInfo(
        patient=state['user_input_info']['patient_name'] != "",
        procedure_guidelines=state['user_input_info']['symptoms'] != [] or state['user_input_info']['disease_name'] != "",
        disease_infos=state['user_input_info']['symptoms'] != [] or state['user_input_info']['disease_name'] != ""
    )

    return {"required_info": required_info}

def router(state: MedicalState, runtime: Runtime) -> str:
    """Route to the next node based on the current state.

    This function determines the next step in the workflow based on the state.

    Args:
        state (MedicalState): The current state of the conversation.
        runtime (Runtime): The runtime context.

    Returns:
        str: The name of the next node to transition to.
    """
    if state.require_patient_info and not state.patient_info:
        return "gather_patient_info"
    elif state.require_procedure_guidelines and not state.procedure_guidelines:
        return "gather_procedure_guidelines"
    elif state.require_disease_info:
        return "gather_disease_info"
    else:
        return "final_diagnosis_and_treatment"