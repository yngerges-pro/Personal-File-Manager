import psycopg2
import db_connection as db

def insert(username, passsword, IP,Port, Status):
    conn = db.connectDataBase()
    sql = "INSERT INTO users (username,password,ip,port,status) VALUES (%s,%s,%s,%s,%s)"
    if conn is None:
            print("Failed to connect to the database.")
            return False
    cur = conn.cursor()
    cur.execute(sql, (username, passsword, IP, Port, Status))
    print("Inserted everthing!")

def update_publicIp(username, public_Ip,port, status):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        update_sql = "UPDATE \"users\" SET ip = %s, status = %s, port =%s WHERE username = %s"  
        cur.execute(update_sql, (public_Ip, status, port, username))
        conn.commit()
        return True
    except psycopg2.Error as e:
        print("Could not update UserIP:", e)
        return False
    finally:
        if conn is not None:
            conn.close()

def check_public_ip(username, current_ip, port, status):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        #select_sql = "SELECT usersip.ip, users.username FROM usersip INNER JOIN users ON users.username = %s"
        select_sql = "SELECT ip FROM \"users\" WHERE username = %s"

        cur.execute(select_sql, (username,))
        user_ip = cur.fetchone()

        if user_ip is not None:
            if user_ip['ip'] != current_ip:
                if update_publicIp(username, current_ip, port, status):
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

