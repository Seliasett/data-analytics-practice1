import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("shop.db")


def run_query(conn: sqlite3.Connection, title: str, sql: str) -> None:
    print(f"\n--- {title} ---")
    cursor = conn.execute(sql)
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()
    print(" | ".join(columns))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(item) for item in row))
    if not rows:
        print("(нет данных)")


def check_database(db_path: Path = DB_PATH) -> None:
    if not db_path.exists():
        raise FileNotFoundError(
            f"Файл {db_path} не найден. Сначала запустите setup_db.py."
        )

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = ["customers", "products", "orders"]
    print("=== Проверка количества записей ===")
    for table in tables:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table};").fetchone()[0]
        print(f"Таблица '{table}': {count} записей")

    total_records = sum(
        cursor.execute(f"SELECT COUNT(*) FROM {t};").fetchone()[0] for t in tables
    )
    print(f"Всего записей во всех таблицах: {total_records}")

    run_query(
        conn,
        "1. Первые 10 заказов с именем клиента, товаром и суммой",
        """
        SELECT
            o.order_id,
            c.full_name AS customer,
            p.title AS product,
            o.quantity,
            (o.quantity * p.price) AS total_amount,
            o.status,
            o.order_date
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        ORDER BY o.order_id
        LIMIT 10;
        """,
    )

    run_query(
        conn,
        "2. Выручка по категориям товаров (только завершённые заказы)",
        """
        SELECT
            p.category,
            COUNT(o.order_id) AS orders_count,
            SUM(o.quantity * p.price) AS revenue
        FROM orders o
        JOIN products p ON o.product_id = p.product_id
        WHERE o.status = 'completed'
        GROUP BY p.category
        ORDER BY revenue DESC;
        """,
    )

    run_query(
        conn,
        "3. Топ покупателей по сумме завершённых покупок",
        """
        SELECT
            c.full_name,
            c.city,
            COUNT(o.order_id) AS completed_orders,
            COALESCE(SUM(o.quantity * p.price), 0) AS total_spent
        FROM customers c
        LEFT JOIN orders o
            ON c.customer_id = o.customer_id AND o.status = 'completed'
        LEFT JOIN products p ON o.product_id = p.product_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC;
        """,
    )

    conn.close()


if __name__ == "__main__":
    check_database()