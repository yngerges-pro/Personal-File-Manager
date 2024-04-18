import psycopg2
from psycopg2.extras import RealDictCursor

def connectDataBase():
    
    DB_NAME = "loginfo"
    DB_USER = "postgres"
    DB_PASS = "6699"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                cursor_factory=RealDictCursor)
        
        
        return conn
    

    except:
        print("Database not connected successfully")
    
def done(bol = False):
    return bol

def createTables(cur, conn):
    try:

        sql = "CREATE TABLE users(ID SERIAL PRIMARY KEY, Username VARCHAR(255) NOT NULL, Password VARCHAR(255) NOT NULL)"
        cur.execute(sql)

        conn.commit()
        done(True)

    except:

        conn.rollback()
        print ("There was a problem during the database creation or the database already exists.")