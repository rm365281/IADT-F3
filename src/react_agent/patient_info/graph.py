from langgraph.graph.state import StateGraph, START

from react_agent.context import Context
from react_agent.patient_info.node import patient_info_retriever, reasoner
from react_agent.state import State

_subgraph_builder = StateGraph(State, context_schema=Context)

_subgraph_builder.add_node(patient_info_retriever)
_subgraph_builder.add_node(reasoner)

_subgraph_builder.add_edge(START, "patient_info_retriever")
_subgraph_builder.add_edge("patient_info_retriever", "reasoner")

patient_info_subgraph = _subgraph_builder.compile(name="patient_info_subgraph")