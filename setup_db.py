import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("shop.db")


def create_and_seed_db(db_path: Path = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Включаем поддержку внешних ключей в SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.executescript(
        """
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            city TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL CHECK (price > 0)
        );

        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        );
        """
    )

    customers = [
        ("Алина Нурланова", "Алматы", "alina.n@example.com"),
        ("Данияр Сериков", "Астана", "daniyar.s@example.com"),
        ("Мария Ким", "Павлодар", "maria.kim@example.com"),
        ("Тимур Ахметов", "Шымкент", "timur.a@example.com"),
        ("Елена Соколова", "Караганда", "elena.s@example.com"),
        ("Арман Омаров", "Актобе", "arman.o@example.com"),
    ]

    products = [
        ("Механическая клавиатура", "Периферия", 24990.0),
        ("Беспроводная мышь", "Периферия", 12500.0),
        ("Монитор 27 дюймов", "Мониторы", 98000.0),
        ("USB-C хаб", "Аксессуары", 8900.0),
        ("Наушники с шумоподавлением", "Аудио", 45000.0),
        ("Подставка для ноутбука", "Аксессуары", 7400.0),
    ]

    # 24 записи в таблице заказов (минимум по заданию — 20)
    orders = [
        (1, 1, 1, "2026-10-01", "completed"),
        (1, 2, 1, "2026-10-02", "completed"),
        (2, 3, 1, "2026-10-03", "completed"),
        (2, 4, 2, "2026-10-04", "completed"),
        (3, 5, 1, "2026-10-05", "completed"),
        (3, 6, 1, "2026-10-06", "pending"),
        (4, 2, 2, "2026-10-07", "completed"),
        (4, 1, 1, "2026-10-08", "cancelled"),
        (5, 3, 1, "2026-10-09", "completed"),
        (5, 4, 1, "2026-10-10", "completed"),
        (6, 5, 1, "2026-10-11", "completed"),
        (6, 2, 1, "2026-10-12", "completed"),
        (1, 6, 2, "2026-10-13", "completed"),
        (2, 1, 1, "2026-10-14", "pending"),
        (3, 2, 1, "2026-10-15", "completed"),
        (4, 5, 1, "2026-10-16", "completed"),
        (5, 6, 1, "2026-10-17", "completed"),
        (6, 3, 1, "2026-10-18", "cancelled"),
        (1, 4, 3, "2026-10-19", "completed"),
        (2, 5, 1, "2026-10-20", "completed"),
        (3, 1, 1, "2026-10-21", "completed"),
        (4, 6, 2, "2026-10-22", "completed"),
        (5, 2, 1, "2026-10-23", "pending"),
        (6, 4, 2, "2026-10-24", "completed"),
    ]

    cursor.executemany(
        "INSERT INTO customers (full_name, city, email) VALUES (?, ?, ?);",
        customers,
    )
    cursor.executemany(
        "INSERT INTO products (title, category, price) VALUES (?, ?, ?);",
        products,
    )
    cursor.executemany(
        """
        INSERT INTO orders (customer_id, product_id, quantity, order_date, status)
        VALUES (?, ?, ?, ?, ?);
        """,
        orders,
    )

    conn.commit()
    conn.close()
    print(f"База данных успешно создана: {db_path}")


if __name__ == "__main__":
    create_and_seed_db()