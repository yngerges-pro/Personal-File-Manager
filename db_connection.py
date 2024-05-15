import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():
    try:
        conn = psycopg2.connect(
            database="loginfo",
            user="postgres",
            password="6699",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        print("Database connected successfully")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def createTables(cur, conn):
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                ID SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                ip VARCHAR,
                port VARCHAR,
                status BOOLEAN
            )
        """)
        conn.commit()
        print("Table 'users' created successfully or already exists")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating table: {e}")
        raise e
