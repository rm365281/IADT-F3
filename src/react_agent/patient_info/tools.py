from langchain_community.agent_toolkits import SQLDatabaseToolkit

from react_agent.patient_info.db_connection import db
from react_agent.utils import load_chat_model

llm = load_chat_model("ollama/llama3.1:8b")

TOOLS = SQLDatabaseToolkit(db=db, llm=llm).get_tools()