from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from src.config.settings import settings
from src.utils.logger import logger

class DatabaseManager:

    def __init__(self):

        logger.info("Initializing database connection...")

        self.engine = create_engine(f"sqlite:///{settings.database_path}")

        self.database = SQLDatabase(self.engine)

        logger.info("Database connected successfully.")

    def get_engine(self):
        return self.engine

    def get_database(self):
        return self.database