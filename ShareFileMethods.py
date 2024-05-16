import os
from pathlib import Path
import pathlib
import psycopg2
import db_connection as db
# import delete_file -- Delete this file later

# Side Methods
def createPath():
    # Will return where this code is at, then add the directory ShareFiles onto path
    return str(pathlib.Path(__file__).parent.resolve()) + "\\ShareFiles"

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """


    if os.path.isfile(file_path):
        # Get Number of bytes
        file_info = os.stat(file_path)
        # Convert bytes to larger units if possible
        return convert_bytes(file_info.st_size)


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

def addNewShareFile(userID, fileName, description):
    conn = db.connectDataBase()
    cur = conn.cursor()
    # Ensure file is not already being shared
    # Either SQL Query for that file, or check keyword.txt
    userID = str(userID)
    description = str(description)

    path = createPath()
    openKeyword = path + "\\keyword.txt"

    filePath = path + "\\" + fileName

    with open(openKeyword, 'r') as file:
        allFiles = file.readlines()
        file.seek(0)
        
        if fileName in allFiles:
            return -1

    # Ensure File Exists in Directory
    # If it exists, Add FileName into keyword.txt
    if pathlib.Path(filePath).is_file():
        with open(openKeyword, 'w') as file:
            file.writelines(fileName)
    else:
        return -2

    # File exists in directory, find the fileSize
    fileSize = file_size(path + "\\" + fileName)
    
    # SQL INSERT new row into files table
    sql = "INSERT INTO files VALUES (%s, %s, %s, %s)"
    val = (userID, fileName, fileSize, description)


    cur.execute(sql, val)
    conn.commit()
    
    cur.close()
    conn.close()
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = File Already Shared
    # -2 = File Not In Directory
    return 1

# def testInsert():
#     print("Inside test insert rn")
#     conn = db.connectDataBase()
#     curr = conn.cursor()

#     sql = "INSERT INTO files VALUES (%s, %s, %s, %s)"
#     val = (int(1), "bigFile", "size big", "garbo")
#     curr.execute(sql, val)
#     conn.commit()
    
#     curr.close()
#     conn.close()
#     return 1
    

def editShareFile(userID, fileName, description):
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

    sql = 'DELETE FROM files WHERE "userid" = ' + userID + ' AND "filename" = ' + fileNameAdjusted
    cur.execute(sql)
    conn.commit()

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

     
    # result is a code here, either successful, or not
    # 1 = success
    # -1 Error

    cur.close()
    conn.close()

    return result

# testInsert()
