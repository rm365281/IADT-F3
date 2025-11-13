from os import name

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from medical_agent.context import Context
from medical_agent.state import InputState, MedicalState

from medical_agent.nodes import normalize_user_input, planning, planning

builder = StateGraph(MedicalState, input_schema=InputState, context_schema=Context)

builder.add_node(normalize_user_input)
builder.add_node(planning)

builder.add_edge(START, "normalize_user_input")
builder.add_edge("normalize_user_input", "planning")
builder.add_edge("planning", END)

graph = builder.compile(name)