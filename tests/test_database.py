from src.database.db_initializer import DatabaseInitializer
from src.database.database_manager import DatabaseManager

def test_database_creation():

    DatabaseInitializer().initialize()

    database = DatabaseManager().get_database()

    tables = database.get_usable_table_names()

    assert "customers" in tables
    assert "orders" in tables
    assert "products" in tables