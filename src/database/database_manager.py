from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from src.config.settings import settings

class DatabaseManager:

    def __init__(self):

        self.engine = create_engine(f"sqlite:///{settings.database_path}")
        self.database = SQLDatabase(self.engine)

    def get_engine(self):
        return self.engine

    def get_database(self):
        return self.database