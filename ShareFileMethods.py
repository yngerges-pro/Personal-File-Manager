import os
import psycopg2
import db_connection as db
import delete_file
# Methods used for Share Files Screen

def viewMyShareFiles(userID):
    conn = db.connectDataBase()
    cur = conn.cursor()
    
    userID = str(userID)
    sql = 'SELECT * FROM files WHERE "UserID" = ' + userID
    cur.execute(sql)
    
    rows = cur.fetchall()
    
    result = []
    
    for row in rows:
        file = {
            'UserID': row['UserID'],
            'FileName': row['FileName'],
            'FileSize': row['FileSize'],
            'Description': row['Description']
        }
        result.append(file)

    cur.close()
    conn.close()
    
    return result

def addNewShareFile(userID, fileName, fileSize, description):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Ensure file is not already being shared
    # Either SQL Query for that file, or check keyword.txt
    userID = str(userID)
    description = str(description)

    path = createPath()
    openKeyword = path + "\\keyword.txt"

    with open(openKeyword, 'r+') as file:
        allFiles = file.readlines()
        file.seek(0)
        file.truncate()
        
        if fileName in allFiles:
            result = -1

    # Ensure File Exists in Directory
    # If it exists, Add FileName into keyword.txt
    if os.path.exists(fileName):
        with open(openKeyword, 'w') as file:
            file.writelines(fileName)
            result = 1
    else:
        result = -2

    # SQL INSERT new row into files table
    sql = 'INSERT INTO files (UserID, FileName, FileSize, Description) VALUES (%s, %s, %s, %s)', (userID, fileName, fileSize, description)
    cur.execute(sql)

    cur.close()
    conn.close()
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = File Already Shared
    # -2 = File Not In Directory
    return result

def editShareFile(userID, fileName, fileSize, description):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Simply SQL UPDATE the row where userID + fileName, update description
    userID = str(userID)

    fileName = str(fileName)
    fileNameAdjusted = "'{}'".format(fileName)

    newDescription = input("Enter new description: ")
    newDescriptionAdjusted = "'{}'".format(newDescription)

    # stop gap, if result's -1 at end, error occurred
    result = -1

    sql = 'UPDATE files SET "Description" = ' + newDescriptionAdjusted + ' WHERE "UserID" = ' + userID + ' AND "FileName" = ' + fileNameAdjusted
    cur.execute(sql)

    result = 1

    cur.close()
    conn.close()
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = Error
    return result

def deleteShareFile(userID, fileName):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Simply SQL DELETE row where userID + fileName
    userID = str(userID)

    fileName = str(fileName)
    fileNameAdjusted = "'{}'".format(fileName)

    sql = 'DELETE FROM files WHERE "UserID" = ' + userID + ' AND "FileName" = ' + fileNameAdjusted
    cur.execute(sql)
    result = -1

    path = createPath()
    openKeyword = path + "\\keyword.txt"

    # Delete line in keyword.txt of fileName
    with open(openKeyword, 'r+') as file:
        allFiles = file.readlines()
        file.seek(0)
        file.truncate()

        for line in allFiles:
            if line.strip("\n") != fileName:
                file.write(line)
                result = 1   

     
    delete_file(userID, fileName)
    # result is a code here, either successful, or not
    # 1 = success
    # -1 Error
    return result

def createPath():
    path = ("Enter main file path: ")
    return path
