from pathlib import Path
from sqlalchemy import create_engine, inspect, text
from langchain_community.utilities import SQLDatabase
from src.config.settings import settings

class DatabaseManager:

    def __init__(self, database_path: Path | None = None):

        path = Path(database_path or settings.database_path).resolve()

        self.engine = create_engine(f"sqlite:///file:{path.as_posix()}?mode=ro&uri=true")
        self.database = SQLDatabase(self.engine)

    def get_engine(self):
        return self.engine

    def get_database(self):
        return self.database

    def get_schema(self) -> dict[str, list[dict]]:

        inspector = inspect(self.engine)

        return {
            table: [
                {"name": column["name"], "type": str(column["type"])}
                for column in inspector.get_columns(table)
            ]
            for table in inspector.get_table_names()
        }

    def run_query(self, query: str) -> tuple[list[str], list[tuple]]:

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return list(result.keys()), [tuple(row) for row in result.fetchall()]
