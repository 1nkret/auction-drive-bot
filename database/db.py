import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from core.config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER


def create_database():
    connection = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='car_app'")
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("CREATE DATABASE car_app")
        print("База данных 'car_app' создана.")
    else:
        print("База данных 'car_app' уже существует.")

    cursor.close()
    connection.close()


def create_tables():
    conn = psycopg2.connect(
        dbname="car_app",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        first_name VARCHAR(50),
        second_name VARCHAR(50),
        phone_number VARCHAR(20)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS filters (
        filter_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
        mark VARCHAR(50),
        model VARCHAR(50),
        year INTEGER CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
        min_mileage INTEGER CHECK (min_mileage >= 0),
        max_mileage INTEGER CHECK (max_mileage >= 0),
        engine_type VARCHAR(10) CHECK (engine_type IN ('petrol', 'electro', 'gibrid', 'dizel')),
        drive_type VARCHAR(10) CHECK (drive_type IN ('front', 'back', 'full')),
        price INTEGER CHECK (price >= 0),
        damage BOOLEAN
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        car_id SERIAL PRIMARY KEY,
        mark VARCHAR(50),
        model VARCHAR(50),
        year INTEGER CHECK (year >= 1900 AND year <= EXTRACT(YEAR FROM CURRENT_DATE)),
        mileage INTEGER CHECK (mileage >= 0),
        engine_type VARCHAR(10) CHECK (engine_type IN ('petrol', 'electro', 'gibrid', 'dizel')),
        drive_type VARCHAR(10) CHECK (drive_type IN ('front', 'back', 'full')),
        price INTEGER CHECK (price >= 0),
        damage BOOLEAN
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Все таблицы созданы.")


if __name__ == "__main__":
    create_database()
    create_tables()
