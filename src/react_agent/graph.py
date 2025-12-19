"""Define a custom Reasoning and Action agent.

Works with a chat model with tool calling support.
"""

from langgraph.graph import StateGraph, START, END

from react_agent.context import Context
from react_agent.nodes import aggregator, clinical_react_orchestrator, disease_info, dummy_node, evaluator, final_answer, out_of_scope_warn, out_of_scope_warn, patient_info, procedure_info, scope_checker
from react_agent.routing_functions import in_scope, requires_disease_info, requires_internal_procedures, requires_patient_data, route_final_answear
from react_agent.state import InputState, State

# Define a new graph

builder = StateGraph(State, input_schema=InputState, context_schema=Context)

builder.add_node(clinical_react_orchestrator)
builder.add_node(patient_info)
builder.add_node(procedure_info)
builder.add_node(disease_info)
builder.add_node(aggregator)
builder.add_node(final_answer)
builder.add_node(evaluator)
builder.add_node(scope_checker)
builder.add_node(dummy_node)
builder.add_node(out_of_scope_warn)

builder.add_edge(START, "clinical_react_orchestrator")
builder.add_edge("clinical_react_orchestrator", "scope_checker")

builder.add_conditional_edges("scope_checker", in_scope, {True: "dummy_node", False: "out_of_scope_warn"})
builder.add_conditional_edges("dummy_node", requires_patient_data, {True: "patient_info"})
builder.add_conditional_edges("dummy_node", requires_internal_procedures, {True: "procedure_info"})
builder.add_conditional_edges("dummy_node", requires_disease_info, {True: "disease_info"})

builder.add_edge("patient_info", "aggregator")
builder.add_edge("procedure_info", "aggregator")
builder.add_edge("disease_info", "aggregator")
builder.add_edge("aggregator", "final_answer")
builder.add_edge("final_answer", "evaluator")

builder.add_conditional_edges("evaluator", route_final_answear)

graph = builder.compile(name="ReAct Agent")
