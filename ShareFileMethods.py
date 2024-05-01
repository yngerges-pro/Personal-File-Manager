import os

# Methods used for Share Files Screen

def viewMyShareFiles(userID, cursorObject):
    userID = str(userID)
    sql = 'SELECT * FROM files WHERE "ID" = ' + userID
    cursorObject.execute(sql)
    result = cursorObject.fetchall()
    return result

def addNewShareFile(userID, fileName, Description, Path, cursorObject):
    # Ensure file is not already being shared
    # Either SQL Query for that file, or check keyword.txt
    userID = str(userID)
    Description = str(Description)
    openKeyword = Path + "\\keyword.txt"

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
    sql = 'INSERT INTO files (ID, FileName, FileSize, Description) VALUES ("userID", "fileName", N/A, "Description")'
    cursorObject.execute(sql)

    # result is a code here, either successful, or not
    # 1 = success
    # -1 = File Already Shared
    # -2 = File Not In Directory
    return result

def editShareFileDescription(userID, fileName, newDescription, cursorObject):
    # Simply SQL UPDATE the row where userID + fileName, update description
    userID = str(userID)
    fileName = str(fileName)
    newDescription = str(newDescription)
    # stop gap, if result's -1 at end, error occurred
    result = -1

    sql = 'UPDATE files SET "Description" = ' + newDescription + ' WHERE "ID" = ' + userID + ' AND "FileName" = ' + fileName
    cursorObject.execute(sql)
    result = 1
    # result is a code here, either successful, or not
    # 1 = success
    # -1 = Error
    return result

def deleteShareFile(userID, fileName, Path, cursorObject):
    # Simply SQL DELETE row where userID + fileName
    userID = str(userID)
    fileName = str(fileName)
    sql = 'DELETE FROM files WHERE "userID" = ' + userID + ' AND "fileName" = ' + fileName
    cursorObject.execute(sql)
    result = -1

    # Delete line in keyword.txt of fileName
    openKeyword = Path + "\\keyword.txt"
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
    return result
