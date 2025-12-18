import uuid

from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage, ToolCall
from lark import logger

from react_agent import state
from react_agent.context import Context
from react_agent.patient_info.tools import TOOLS
from react_agent.state import State
from react_agent.utils import load_chat_model

import asyncio
import logging

logger = logging.getLogger(__name__)

async def patient_info_retriever(state: State):
   """
   Placeholder for patient info retriever logic.
   """
   logger.info(f"Patient Info Retriever invoked with patient_name: {state['patient_name']}")

   tool_call = ToolCall(
      name="sql_db_query",
      args={"query": "SELECT * FROM patients WHERE full_name LIKE '%{}%';".format(state['patient_name'])},
      id=uuid.uuid4().hex,
      type="tool_call"
   )

   tool_call_message = AIMessage(content="", tool_calls=[tool_call])

   run_query_tool = next(tool for tool in TOOLS if tool.name == "sql_db_query")
   tool_message = await run_query_tool.ainvoke(tool_call)
   response = AIMessage(f"Patient info: {tool_message.content}")

   return {"messages": [tool_call_message, tool_message, response]}

async def reasoner(state: State, runtime: Runtime[Context]):
   """
   Reasoner node that processes patient information and generates a response.
   """
   system_message = SystemMessage(content="""
      You are a medical assistant helping to gather patient information based on database queries.
      Use the information from the database queries to compile a summary of the patient's medical data.
      Provide clear and concise information without making assumptions or adding unverified details.
                                  
      If no data is found, state that explicitly.
                                  
      DO NOT CREATE ANY NEW INFORMATION.
   """)

   model = await asyncio.to_thread(load_chat_model, runtime.context.model)
   response = await model.ainvoke([system_message] + state['messages'])

   logger.info(f"Reasoner response: {response}")

   return {"patient_data": response.content}