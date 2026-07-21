from src.agent.sql_agent import SQLAgent
from src.utils.logger import logger
from src.utils.exceptions import (QueryExecutionError, SQLAssistantError)

class SQLService:

    def __init__(self):

        logger.info("Initializing SQLService...")

        self.agent = SQLAgent()

    def ask(self, question: str) -> str:

        if not question.strip():
            raise QueryExecutionError("The question cannot be empty.")

        try:
            logger.info("Processing user question...")

            return self.agent.ask(question)
        except SQLAssistantError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise QueryExecutionError("Failed to process the request.") from e