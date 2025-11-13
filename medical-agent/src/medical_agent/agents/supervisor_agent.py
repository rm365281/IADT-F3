from langchain_ollama import ChatOllama
from agents import pdf_agent, sql_agent
from langchain.tools import tool
from langchain.agents import create_agent

model = ChatOllama(model="gpt-oss:20b")

@tool
def patient_query(query: str) -> str:
    """Query the medical records database using SQL and return the results as a JSON string.
    
    Use this tool to perform read-only SQL queries on the medical records database.
    Ensure that the query does not modify any data (no INSERT, UPDATE, DELETE, etc.).

    Input: Patient name
    """
    result = sql_agent.invoke(
        {"messages":[{"role":"user", "content": query}]}
    )
    return result["messages"][-1].text

@tool
def procedure_search(query: str) -> str:
    """Search hospital procedures based on the user's query and return relevant information.
    
    Use this tool to find and summarize hospital procedures that match the user's request.

    Input: Condition or procedure name
    """
    result = pdf_agent.invoke(
        {"messages":[{"role":"user", "content": query}]}
    )
    return result["messages"][-1].text

SUPERVISOR_PROMPT = (
    "You are a medical supervisor agent. Your role is to assist healthcare professionals "
    "by providing accurate information from patient records and hospital procedures. "
    "Use the provided tools to query patient data and search for hospital procedures as needed. "
    "Always ensure patient privacy and data security in your responses."
)

supervisor_agent = create_agent(
    model=model,
    tools=[
        patient_query,
        procedure_search
    ],
    system_prompt=SUPERVISOR_PROMPT
)