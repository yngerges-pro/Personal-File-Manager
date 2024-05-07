import psycopg2
import db_connection as db

def update_publicIp(username, public_Ip):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        update_sql = "UPDATE \"usersIP\" SET ip = %s WHERE username = %s"
        cur.execute(update_sql, (public_Ip, username))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print("Could not update UserIP:", e)
        return False
    finally:
        if conn is not None:
            conn.close()

def check_public_ip(username, current_ip):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        select_sql = "SELECT ip FROM \"usersIP\" WHERE username = %s"
        cur.execute(select_sql, (username,))
        user_ip = cur.fetchone()

        if user_ip is not None:
            if user_ip['ip'] != current_ip:
                if update_publicIp(username, current_ip):
                    print("Public IP's do not Match!")
                    print("Updated user's public IP!")
                else:
                    print("Cannot Update user's public IP.")
        else:
            print("User's IP record not found in the database.")

        return True
    except psycopg2.Error as e:
        print("Error checking user's IP:", e)
        return False
    finally:
        if conn is not None:
            conn.close()
