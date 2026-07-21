from src.database.db_initializer import DatabaseInitializer
from src.services.sql_service import SQLService
from src.utils.exceptions import SQLAssistantError
from src.utils.logger import logger

def main():

    logger.info("Starting SQL AI Assistant...")

    DatabaseInitializer().initialize()

    service = SQLService()

    while True:

        question = input("\nAsk a question (or type 'exit'): ")

        if question.lower() == "exit":
            break

        try:
            answer = service.ask(question)

            print("\nAnswer:")
            print(answer)
        except SQLAssistantError as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()