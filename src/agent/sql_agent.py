from langchain.agents import AgentType
from langchain_community.agent_toolkits import create_sql_agent
from src.database.database_manager import DatabaseManager
from src.llm.openai_client import OpenAIClient
from src.utils.logger import logger

class SQLAgent:

    def __init__(self):

        logger.info("Initializing SQL Agent...")

        self.database = DatabaseManager().get_database()

        self.llm = OpenAIClient().get_model()

        self.agent = self._create_agent()

        logger.info("SQL Agent initialized successfully.")

    def _create_agent(self):
        prefix = """
You are an expert SQL assistant.

Always:
- Generate valid SQLite SQL.
- Never modify the database.
- Use only SELECT statements.
- Use the available tables only.
- Return concise answers.
"""

        return create_sql_agent(
            llm=self.llm,
            db=self.database,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
            prefix=prefix
        )
    
    def ask(self, question: str):

        logger.info(f"Question received: {question}")

        response = self.agent.invoke(
            {
                "input": question
            }
        )

        return response["output"]