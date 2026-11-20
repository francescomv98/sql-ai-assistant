from pathlib import Path
import sqlite3
from src.config.settings import settings
from src.utils.logger import logger

class DatabaseInitializer:

    def __init__(self, database_path: Path | None = None):

        self.database_path = Path(database_path or settings.database_path)

    def initialize(self):

        database_path = self.database_path

        if database_path.exists():
            logger.info("Database already exists.")
            return

        logger.info("Creating SQLite database...")

        database_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = database_path.with_suffix(database_path.suffix + ".tmp")
        temp_path.unlink(missing_ok=True)

        connection = sqlite3.connect(temp_path)

        try:
            self._create_tables(connection)
            self._insert_sample_data(connection)

            connection.commit()
        except Exception:
            connection.close()
            temp_path.unlink(missing_ok=True)
            raise

        connection.close()
        temp_path.replace(database_path)

        logger.info("Database successfully created.")

    def _create_tables(self, connection):

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE customers(
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city TEXT NOT NULL
        )""")
        
        cursor.execute("""
        CREATE TABLE products(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )""")

        cursor.execute("""
        CREATE TABLE orders(
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )""")

        cursor.execute("""
        CREATE TABLE order_items(
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )""")

    def _insert_sample_data(self, connection):
        cursor = connection.cursor()

        customers = [
            (1, "Alice", "Rossi", "Rome"),
            (2, "Marco", "Bianchi", "Milan"),
            (3, "Laura", "Verdi", "Turin"),
            (4, "John", "Smith", "London"),
            (5, "Emma", "Brown", "Paris")
        ]

        cursor.executemany(
            """
            INSERT INTO customers
            VALUES (?, ?, ?, ?)
            """,
            customers
        )

        products = [
            (1, "Laptop", "Electronics", 1200),
            (2, "Phone", "Electronics", 850),
            (3, "Tablet", "Electronics", 600),
            (4, "Monitor", "Electronics", 300),
            (5, "Keyboard", "Accessories", 80),
            (6, "Mouse", "Accessories", 45),
            (7, "Headphones", "Accessories", 150),
            (8, "Printer", "Office", 250),
            (9, "Desk", "Furniture", 400),
            (10, "Office Chair", "Furniture", 320)
        ]

        cursor.executemany(
            """
            INSERT INTO products
            VALUES (?, ?, ?, ?)
            """,
            products
        )

        orders = [
            (1,1,"2023-11-15"),
            (2,2,"2023-12-02"),
            (3,3,"2024-01-10"),
            (4,4,"2024-01-18"),
            (5,5,"2024-02-05"),
            (6,1,"2024-02-20"),
            (7,2,"2024-03-08"),
            (8,3,"2024-03-19"),
            (9,4,"2024-04-02"),
            (10,5,"2024-04-18"),
            (11,1,"2024-05-05"),
            (12,2,"2024-05-21"),
            (13,3,"2024-06-10"),
            (14,4,"2024-06-22"),
            (15,5,"2024-07-01"),
            (16,1,"2024-07-15"),
            (17,2,"2024-08-03"),
            (18,3,"2024-08-19"),
            (19,4,"2024-09-05"),
            (20,5,"2024-09-23"),
            (21,1,"2024-10-08"),
            (22,2,"2024-10-24"),
            (23,3,"2024-11-12"),
            (24,4,"2024-11-28"),
            (25,5,"2024-12-10"),
            (26,1,"2025-01-07"),
            (27,2,"2025-02-01"),
            (28,3,"2025-02-18"),
            (29,4,"2025-03-04"),
            (30,5,"2025-03-20")
        ]

        cursor.executemany(
            """
            INSERT INTO orders
            VALUES (?, ?, ?)
            """,
            orders
        )

        order_items = [
            (1,1,1,1200),(1,5,1,80),
            (2,2,2,850),(2,6,2,45),
            (3,3,1,600),(3,5,1,80),
            (4,4,2,300),(4,7,1,150),
            (5,1,1,1200),(5,10,1,320),
            (6,2,1,850),(6,6,1,45),
            (7,8,1,250),(7,5,2,80),
            (8,9,1,400),(8,10,1,320),
            (9,3,2,600),(9,7,1,150),
            (10,4,1,300),(10,5,1,80),
            (11,2,1,850),(11,6,2,45),
            (12,1,1,1200),(12,7,1,150),
            (13,3,1,600),(13,8,1,250),
            (14,9,1,400),(14,5,1,80),
            (15,10,1,320),(15,6,1,45),
            (16,1,1,1200),(16,4,1,300),
            (17,2,1,850),(17,7,1,150),
            (18,8,2,250),(18,5,1,80),
            (19,9,1,400),(19,10,1,320),
            (20,3,1,600),(20,6,2,45),
            (21,1,2,1200),(21,5,1,80),
            (22,2,1,850),(22,8,1,250),
            (23,4,1,300),(23,7,2,150),
            (24,9,1,400),(24,6,1,45),
            (25,10,2,320),(25,5,2,80),
            (26,1,1,1200),(26,2,1,850),
            (27,3,1,600),(27,4,1,300),
            (28,5,3,80),(28,6,2,45),
            (29,8,1,250),(29,9,1,400),
            (30,10,1,320),(30,7,1,150)
        ]

        cursor.executemany(
            """
            INSERT INTO order_items
            VALUES (?, ?, ?, ?)
            """,
            order_items
        )