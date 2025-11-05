import logging
import os

from langchain.agents import create_agent
from langchain_classic import hub
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama

from agents.custom_guardrail import DatabaseWriteOperationGuardrail

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'test_db')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


logging.info("Initializing Ollama LLM...")
llm = ChatOllama(model="gpt-oss:20b")
logging.info("Ollama LLM initialized.")

logging.info("Setting up database connection...")
db = SQLDatabase.from_uri(
    database_uri=f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}",
)
logging.info("Database connection established.")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prompt_template = hub.pull("langchain-ai/sql-agent-system-prompt")
system_message = prompt_template.format(dialect="MySQL", top_k=5)

agent = create_agent(
    model=llm,
    tools=toolkit.get_tools(),
    system_prompt=system_message,
    middleware=[
        DatabaseWriteOperationGuardrail()
    ]
)