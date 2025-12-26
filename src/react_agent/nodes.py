import asyncio
import datetime
import logging
from typing import Dict, List

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langgraph.types import Overwrite
from langgraph.runtime import Runtime
from langchain.agents import create_agent

from react_agent.context import Context
from react_agent.schemas import Feedback, UserInputInfo
from react_agent.utils import load_chat_model, load_openai_model
from react_agent.state import State

logger = logging.getLogger(__name__)

async def clinical_react_orchestrator(state: State, runtime: Runtime[Context]) -> Dict[str, List[AIMessage]]:
    """
    Orchestrator node: Plans and routes sub-tasks to worker nodes based on user request.
    Calls the LLM to determine next actions and updates the conversation state.
    """
    logger.debug("Invoking clinical_react_orchestrator node")
    messages = state.get('messages', [])

    model = load_chat_model(runtime.context.model).with_structured_output(UserInputInfo)
    system_message = runtime.context.system_prompt

    response = await model.ainvoke(
        [{"role": "system", "content": system_message}, *messages]
    )

    logger.info(f"Orchestrator response: {response}")

    return {
        "require_patient_data": response['patient'],
        "require_internal_procedures": response['internal_procedures'],
        "require_disease_info": response['disease_info'],
        "patient_name": response['patient_name'],
        "symptoms": response['symptoms'],
        "disease_name": response['disease_name'],
        "condition": response['condition'],
        "medical_procedure": response['medical_procedure'],
    }

def scope_checker(state: State) -> State:
    """
    Check if the user query is within the scope of the agent's capabilities.
    """
    return {
        "in_scope": state.get('require_patient_data', False) or
                    state.get('require_internal_procedures', False) or
                    state.get('require_disease_info', False)
    }

def dummy_node(state: State) -> State:
    """
    A dummy node that does nothing.
    """
    return state
    
def out_of_scope_warn(state: State) -> State:
    """
    Handle out-of-scope queries.
    """
    
    system_message = """
    I'm sorry, but your request is outside the scope of my capabilities, and I am unable to assist with it.\n
    My functions are limited to:
     - Providing information and assistance related to clinical and medical topics based on the data I have access to.
     - Answering questions about diseases, symptoms, and medical procedures within my knowledge base.
     - Search patient information from the internal database when provided with valid identifiers.
    """

    return {
        "messages": [AIMessage(content=system_message)]
    }

async def patient_info(state: State, runtime: Runtime[Context]) -> State:
    """
    Worker node: Handles SQL queries for patient data.
    """
    db = await asyncio.to_thread(SQLDatabase.from_uri, database_uri=runtime.context.mysql_connection_string)
    engine = db._engine

    rows = await asyncio.to_thread(find_patients_by_name, engine, state['patient_name'])

    patient_context = await asyncio.to_thread(patients_to_context, rows)
    return {"patient_data": patient_context}

from sqlalchemy import text

def find_patients_by_name(engine, patient_name: str):
    query = text("""
        SELECT
            id,
            full_name,
            birth_date,
            gender,
            created_at,
            updated_at
        FROM patients
        WHERE full_name LIKE :name
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"name": f"%{patient_name}%"}
        )
        return result.fetchall()

def patients_to_context(rows) -> str:
    if not rows:
        return "No patient records were found."

    lines = []

    for (
        patient_id,
        full_name,
        birth_date,
        gender,
        created_at,
        updated_at,
    ) in rows:

        lines.append(
            f"""
- ID: {patient_id}
- Name: {full_name}
- Birth date: {birth_date}
- Gender: {gender.capitalize()}
- Created at: {created_at:%Y-%m-%d %H:%M}
- Updated at: {updated_at:%Y-%m-%d %H:%M}
- Age: {(datetime.datetime.now().year - birth_date.year) if birth_date else 'Unknown'}
""".strip()
        )

    return "\n\n".join(lines)


async def procedure_info(state: State, runtime: Runtime[Context]) -> State:
    """
    Worker node: Handles vector DB search for internal medical procedures.
    """
    from react_agent.tools import retrieve_procedure_info
    import asyncio
    model = await asyncio.to_thread(load_chat_model, runtime.context.model)

    system_prompt = runtime.context.procedure_info_query_prompt
    agent = create_agent(model, [retrieve_procedure_info], system_prompt=system_prompt)
    response = await agent.ainvoke({"messages": state['medical_procedure']})

    logger.info(f"Vector search response: {response}")
    logger.info(f"Vector search output: {response['messages'][-1]}")
    logger.info(f"Vector search content: {response['messages'][-1].content}")

    return {"internal_procedures_data": response['messages'][-1].content}

async def disease_info(state: State, runtime: Runtime[Context]) -> State:
    """
    Worker node: Handles disease information queries via LLM.
    """
    model = await asyncio.to_thread(load_openai_model, runtime.context.medical_model, runtime.context.open_ai_url)

    system_prompt = runtime.context.disease_diagnosis_prompt

    human_prompt = """
    Disease: "{disease_name}".
    
    Symptoms "{symptoms}".
    """.format(disease_name=state['disease_name'], symptoms=", ".join(state['symptoms']))

    humanMessage = HumanMessage(content=human_prompt)

    logger.info(f"Disease model human message: {humanMessage}")

    result = await model.ainvoke([SystemMessage(content=system_prompt), humanMessage])

    logger.info(f"Disease model result: {result}")

    return {"disease_info_data": result.content}

async def aggregator(state: State) -> State:
    """
    Aggregator node: Merges data from multiple sources into the state.
    """
    logger.info("Aggregating data from worker nodes")
    logger.info(f"Current state: {state}")

    patient_details = state.get('patient_data', "")
    internal_procedures = state.get('internal_procedures_data', "")
    disease_info = state.get('disease_info_data', "")

    combined_output = await asyncio.to_thread(lambda: f"Patient Details:\n{patient_details}\n\nInternal Medical Procedures:\n{internal_procedures}\n\nDisease Information:\n{disease_info}")

    return {"combined_output": Overwrite(combined_output)}

async def wait(state: State) -> State:
    """
    A placeholder await function to satisfy async requirements.
    """
    return state

def final_answer(state: State, runtime: Runtime[Context]) -> dict:
    """
    Worker node: Formats and returns the final answer using the LLM.
    """

    logger.info("Generating final answer...")
    logger.info(f"Combined output: {state['combined_output']}")

    llm = load_chat_model(runtime.context.model)
    response = llm.invoke([
        SystemMessage(content=runtime.context.final_answer_prompt),
        HumanMessage(content=state["combined_output"]),
        *state['messages']
    ])
    return {
        "messages": [response]
    }

def evaluator(state: State, runtime: Runtime[Context]):
    """
    Evaluate model responses for quality and relevance.
    """

    messages = state.get('messages', [])
    model_response = messages[-1].content if messages and hasattr(messages[-1], 'content') else ""

    print("Evaluating model response...", model_response)

    system_prompt = runtime.context.evaluation_prompt

    model = load_chat_model(runtime.context.model)
    structured_model = model.with_structured_output(Feedback)
    feedback = structured_model.invoke(
        [{"role": "system", "content": system_prompt}, *messages]
    )
    print("Evaluator feedback:", feedback)

    return {"feedback": feedback}