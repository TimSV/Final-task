import os
import time
import psycopg2
from psycopg2 import OperationalError
import dotenv

dotenv.load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", 5432)
}


def wait_for_db():
    """Ожидание доступности PostgreSQL"""
    print("Подключение к БД...")
    retries = 0
    while retries < 10:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print("База данных готова!")
            return
        except OperationalError as e:
            print(f"Ошибка подключения к БД: {e}")
            retries += 1
            print(f"Повтор через 5 сек... ({retries}/10)")
            time.sleep(5)
    raise Exception("Не удалось подключиться к БД после 10 попыток")


def create_tables():
    """Создание таблиц"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            score INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
    )

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Таблицы успешно созданы")
    except (Exception, OperationalError) as e:
        print(f"Ошибка при создании таблиц: {e}")
        raise
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    wait_for_db()
    create_tables()
