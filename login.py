import psycopg2
import db_connection as db

def getloginData(username, password):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False
        
        cur = conn.cursor()
        cur.callproc("check_user_credentials", (username, password))  # Call the stored procedure

        # Fetch all results of the function call
        rows = cur.fetchall()
        
        # Get the value of 'check_user_credentials' from the first dictionary
        result = rows[0]['check_user_credentials']
        
        return result
    
    except psycopg2.Error as e:
        print("Error executing SQL query:", e)
        return False
    finally:
        if conn is not None:
            conn.close()