import logging
import time
from dataclasses import dataclass, field
from langchain_community.agent_toolkits import create_sql_agent
from src.database.database_manager import DatabaseManager
from src.llm.openai_client import OpenAIClient
from src.utils.logger import logger
from src.utils.exceptions import SQLAgentError

SQL_QUERY_TOOL = "sql_db_query"

@dataclass
class AgentResponse:
    answer: str
    queries: list[str] = field(default_factory=list)
    elapsed_time: float = 0.0

    @property
    def final_query(self) -> str | None:
        return self.queries[-1] if self.queries else None

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

Your task is to answer user questions by querying a SQLite database.

Rules:

- Generate only valid SQLite SQL.
- Never modify the database.
- Never use INSERT.
- Never use UPDATE.
- Never use DELETE.
- Never use DROP.
- Only retrieve the data needed.
- If the answer cannot be found, say so.
"""

        return create_sql_agent(
            llm=self.llm,
            db=self.database,
            agent_type="tool-calling",
            verbose=logger.isEnabledFor(logging.DEBUG),
            prefix=prefix,
            agent_executor_kwargs={"return_intermediate_steps": True}
        )

    def ask(self, question: str) -> AgentResponse:

        logger.info(f"Question received: {question}")

        try:
            start_time = time.time()

            response = self.agent.invoke(
                {
                    "input": question
                }
            )

            elapsed_time = time.time() - start_time

            logger.info(f"SQL Agent completed in {elapsed_time:.2f}s")

            queries = self._extract_queries(response.get("intermediate_steps", []))

            for query in queries:
                logger.debug(f"Executed SQL: {query}")

            return AgentResponse(
                answer=response["output"],
                queries=queries,
                elapsed_time=elapsed_time
            )
        except Exception as e:
            logger.error(f"SQL Agent execution failed: {e}")
            raise SQLAgentError("Unable to process SQL request.") from e

    @staticmethod
    def _extract_queries(steps) -> list[str]:

        queries = []

        for action, _ in steps:

            if getattr(action, "tool", None) != SQL_QUERY_TOOL:
                continue

            tool_input = action.tool_input

            if isinstance(tool_input, dict):
                tool_input = tool_input.get("query", "")

            if tool_input:
                queries.append(str(tool_input).strip())

        return queries
