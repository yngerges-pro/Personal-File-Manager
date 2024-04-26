import psycopg2
# Methods used for Share Files Screen

def viewMyShareFiles(userID, dataBase):
    conn = dataBase.connectDatabase
    cur = conn.cursor()
    
    userID = str(userID)
    sql = 'SELECT * FROM files WHERE "ID" = ' + userID
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

def addNewShareFile(userID, fileName, Description, Path, cursorObject):
    # Ensure file is not already being shared
    # Either SQL Query for that file, or check keyword.txt

    # Ensure File Exists in Directory

    # If it exists, Add FileName into keyword.txt

    # SQL INSERT new row into files table
    sql = ""

    # result is a code here, either successful, or not
    # 1 = success
    # -1 = File Already Shared
    # -2 = File Not In Directory
    return result

def editShareFileDescription(userID, fileName, newDescription, cursorObject):
    # Simply SQL UPDATE the row where userID + fileName, update description
    sql = ""

    # result is a code here, either successful, or not
    # 1 = success
    # -1 = Error
    return result

def deleteShareFile(userID, fileName, Path, cursorObject):
    # Simply SQL DELETE row where userID + fileName
    sql = ""

    # Delete line in keyword.txt of fileName

    # result is a code here, either successful, or not
    # 1 = success
    # -1 Error
    return result
