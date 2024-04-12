import db_connection as db

def getloginData():
    conn = db.connectDataBase()
    # Create a cursor object
    cur = conn.cursor()

    # SQL query to retrieve Username and Password
    sql = "SELECT Username, Password FROM users"

    # Execute the query
    cur.execute(sql)

    # Fetch all rows
    rows = cur.fetchall() #diction = {username : User, password : jkljkl, username : User2, password: fdkajkl;,...}
    print("rows:", rows)
    for r in rows:
        username, password = r
        print("Username:", username)
        print("Password:", password)
        return username, password
