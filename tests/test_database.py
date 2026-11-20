import pytest
from sqlalchemy.exc import OperationalError
from src.database.db_initializer import DatabaseInitializer
from src.database.database_manager import DatabaseManager

@pytest.fixture
def database_path(tmp_path):

    path = tmp_path / "sales.db"

    DatabaseInitializer(path).initialize()

    return path

def test_database_creation(database_path):

    database = DatabaseManager(database_path).get_database()

    tables = database.get_usable_table_names()

    assert "customers" in tables
    assert "orders" in tables
    assert "products" in tables
    assert "order_items" in tables

def test_initialize_is_idempotent(database_path):

    DatabaseInitializer(database_path).initialize()

    columns, rows = DatabaseManager(database_path).run_query("SELECT COUNT(*) FROM customers")

    assert rows == [(5,)]

def test_failed_initialization_leaves_no_database(tmp_path, monkeypatch):

    path = tmp_path / "sales.db"
    initializer = DatabaseInitializer(path)

    def fail(connection):
        raise RuntimeError("boom")

    monkeypatch.setattr(initializer, "_insert_sample_data", fail)

    with pytest.raises(RuntimeError):
        initializer.initialize()

    assert not path.exists()
    assert not path.with_suffix(".db.tmp").exists()

def test_run_query_returns_columns_and_rows(database_path):

    columns, rows = DatabaseManager(database_path).run_query(
        "SELECT name, price FROM products WHERE name = 'Laptop'"
    )

    assert columns == ["name", "price"]
    assert rows == [("Laptop", 1200.0)]

def test_database_is_read_only(database_path):

    manager = DatabaseManager(database_path)

    with pytest.raises(OperationalError):
        manager.run_query("DELETE FROM customers")

    assert manager.run_query("SELECT COUNT(*) FROM customers")[1] == [(5,)]

def test_get_schema(database_path):

    schema = DatabaseManager(database_path).get_schema()

    assert [column["name"] for column in schema["products"]] == ["id", "name", "category", "price"]
