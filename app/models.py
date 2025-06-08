import os
import psycopg2

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", 5432)
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def save_user(name: str, score: int):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (name, score)
            VALUES (%s, %s)
            RETURNING id, name, score, timestamp
            """,
            (name, score)
        )
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {
            "id": result[0],
            "name": result[1],
            "score": result[2],
            "timestamp": result[3].isoformat()  # Преобразуем дату в ISO-формат
        }
    except Exception as e:
        raise e


def get_all_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name, score, timestamp FROM users")
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()

        # Преобразуем результат в список словарей
        return [
            {
                "id": row[0],
                "name": row[1],
                "score": row[2],
                "timestamp": row[3].isoformat()
            } for row in rows
        ]
    except Exception as e:
        raise e