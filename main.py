from src.database.db_initializer import DatabaseInitializer
from src.services.sql_service import SQLService
from src.utils.exceptions import SQLAssistantError
from src.utils.logger import logger

EXIT_COMMANDS = {"exit", "quit"}

def main():

    logger.info("Starting SQL AI Assistant...")

    DatabaseInitializer().initialize()

    service = SQLService()

    while True:

        try:
            question = input("\nAsk a question (or type 'exit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not question:
            continue

        if question.lower() in EXIT_COMMANDS:
            break

        try:
            response = service.ask(question)

            if response.final_query:
                print("\nSQL:")
                print(response.final_query)

            print("\nAnswer:")
            print(response.answer)
        except SQLAssistantError as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
