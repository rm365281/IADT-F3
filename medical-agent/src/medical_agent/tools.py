from typing import Any, Callable, List

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.runtime import get_runtime
from medical_agent.context import Context
from utils import load_chat_model

"""This module provides medical-related tools for the medical agent.
These tools are intended to be used by the medical agent to assist with various tasks.
"""

runtime = get_runtime(Context)



TOOLS: List[Callable[..., Any]] = SQLDatabaseToolkit(db=runtime.context.sql_db_connection, llm=load_chat_model(runtime.context.sql_model)).get_tools() + [
    
]