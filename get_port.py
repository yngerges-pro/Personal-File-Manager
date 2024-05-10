import psycopg2
import db_connection as db


#please add from get_port import get_port to main.py
#and get_port import get_CurrentIP to main.py
#PLEASE add get_port(Cuser) and get_CurrentIP(Cuser)to main.py after the line update_publicIp(Cuser, current_ip)  #Updates

def get_port(username):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return None
        cur = conn.cursor()
        port_sql = "SELECT port FROM \"usersIP\" WHERE username = %s"
        cur.execute(port_sql, (username,))
        user_port = cur.fetchone()


        if user_port is not None:
            print("User's Port:", user_port['port'])
        else:
            print("Username does not match Port.")
 

            
    except psycopg2.Error as e:
        print("Error retrieving user's port:", e)
        return None

    finally:
        if conn is not None:
            conn.close()

def get_CurrentIP(username):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return None
        cur = conn.cursor()
        currentIp_sql = "SELECT ip FROM \"usersIP\" WHERE username = %s"
        cur.execute(currentIp_sql, (username,))
        currentIp = cur.fetchone()    
        if currentIp is not None:
            print("User's Current Ip:", currentIp['ip'])
        else:
            print("Could not get User's Current Ip.")  

    except psycopg2.Error as e:
        print("Error retrieving user's Current Ip:", e)
        return None

    finally:
        if conn is not None:
            conn.close()     
            



