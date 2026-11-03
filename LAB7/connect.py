import psycopg2
from config import load_config

def get_connection():
    try:
        config = load_config()
        conn = psycopg2.connect(**config)
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Ошибка подключения к БД: {error}")
        return None

if __name__ == '__main__':
    conn = get_connection()
    if conn:
        print('Connected to the PostgreSQL server.')
        conn.close()