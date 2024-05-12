import psycopg2
import db_connection as db


def user_status(username, change_status):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False
        cur = conn.cursor()
        status_sql = "UPDATE \"users\" SET status = %s WHERE username = %s"
        cur.execute(status_sql, (change_status, username,)) #change status to true 
        conn.commit()
        print("User is now ONLINE")
        return True
    except psycopg2.Error as e:
        print("Could not update Status:", e)
        return False
    finally:
        if conn is not None:
            conn.close()

def not_logged_in(username, change_status):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False
    
        cur = conn.cursor()
        status_sql = "UPDATE \"users\" SET status = %s WHERE username = %s"
        cur.execute(status_sql, (change_status,username,)) #change status to False
        conn.commit()
        print("User is now OFFLINE")
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False
    finally:
        if conn:
            conn.close()


