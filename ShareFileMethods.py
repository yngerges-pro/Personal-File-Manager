import psycopg2
import db_connection as db
# Methods used for Share Files Screen

def viewMyShareFiles(user):
    conn = db.connectDataBase()
    cur = conn.cursor()
    
    userID = str(user)
    sql = 'SELECT * FROM files WHERE "userid" = ' + userID
    cur.execute(sql)
    
    rows = cur.fetchall()
    
    result = []
    
    for row in rows:
        file = {
            'UserID': row['userid'],
            'FileName': row['filename'],
            'FileSize': row['filesize'],
            'Description': row['description']
        }
        result.append(file)

    cur.close()
    conn.close()
    
    return result

def addNewShareFile(userID, fileName, Description, Path):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Ensure file is not already being shared
    # Either SQL Query for that file, or check keyword.txt

    # Ensure File Exists in Directory

    # If it exists, Add FileName into keyword.txt

    # SQL INSERT new row into files table
    sql = ""

    
    cur.close()
    conn.close()
    
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = File Already Shared
    # -2 = File Not In Directory
    
    return result

def editShareFileDescription(userID, fileName, newDescription):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Simply SQL UPDATE the row where userID + fileName, update description
    sql = ""

    cur.close()
    conn.close()
    
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = Error
    return result

def deleteShareFile(userID, fileName, Path):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Simply SQL DELETE row where userID + fileName
    sql = ""

    # Delete line in keyword.txt of fileName

    cur.close()
    conn.close()
    
    # result is a code here, either successful, or not
    # 1 = success
    # -1 Error
    return result
