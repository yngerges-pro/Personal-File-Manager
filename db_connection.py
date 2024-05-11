import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():
    try:
        conn = psycopg2.connect(
            database="loginfo",
            user="postgres",
            password="123",
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
                Username VARCHAR(255) NOT NULL,
                Password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        print("Table 'users' created successfully or already exists")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating table: {e}")
        raise e
