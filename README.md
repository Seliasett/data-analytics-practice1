# День 1: Создание базы данных SQLite (`data-analytics-practice`)

## Описание работы
В рамках первого дня практики создана реляционная база данных интернет-магазина `shop.db` в **SQLite** с тремя связанными таблицами:
- `customers` — покупатели (`customer_id`, `full_name`, `city`, `email`);
- `products` — товары (`product_id`, `title`, `category`, `price`);
- `orders` — заказы (`order_id`, `customer_id`, `product_id`, `quantity`, `order_date`, `status`).

В таблице `orders` размещено **24 записи** (что превышает минимальное требование в 20 записей).

## Состав репозитория
- `setup_db.py` — скрипт создания схемы БД и заполнения её тестовыми данными.
- `check_db.py` — скрипт проверки целостности данных, подсчёта записей и выполнения аналитических SQL-запросов.
- `shop.db` — готовый файл базы данных SQLite.
- `README.md` — описание проекта и инструкция по запуску.

## Запуск
```bash
python setup_db.py
python check_db.py