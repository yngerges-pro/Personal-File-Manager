# Methods used for the Download Files Screen
import pathlib
import db_connection as db
from ReceivingSide import *

def getDownloadPath():
    # Get path to this code file, remove code name and add directory to ReceiveFile directory
    return str(pathlib.Path(__file__).parent.resolve()) + "\\ReceiveFiles"


def viewAllDownloadableFiles():
    conn = db.connectDataBase()
    curr = conn.cursor()

    # Need to join files table and users tables, only return where
    # Status = true in usersip
    sql = 'SELECT * FROM files'

    curr.execute(sql)
    rows = curr.fetchall()

    result = []
    
    for row in rows:
        file = {
            'UserID': row['userid'],
            'FileName': row['filename'],
            'FileSize': row['filesize'],
            'Description': row['description']
        }
        result.append(file)
    
    conn.close()
    curr.close()

    # result is a list
    return result

def searchForDownloadableFiles(searchWith):
    conn = db.connectDataBase()
    curr = conn.cursor()

    searchWith = "%" + searchWith + "%" # Add wild cards front and back of searching with
    sql = "SELECT f.FileName, f.FileSize, f.Description FROM files f JOIN users u ON u.status = true AND fileName = " + searchWith

    rows = curr.execute(sql)

    result = []
    
    for row in rows:
        file = {
            'FileName': row['FileName'],
            'FileSize': row['FileSize'],
            'Description': row['Description']
        }
        result.append(file)

    
    conn.close()
    curr.close()
    # Need to join files table and usersip table together, only return where
    # Status = true AND LIKE fileName = searchWith
    # result is a list
    return result

def downloadThisFile (fileName):
    # SQL query users table, grab IP and Port
    conn = db.connectDataBase()
    curr = conn.cursor()

    downloadPath = getDownloadPath()
    
    # sql = 'SELECT ip, port FROM users JOIN files ON users.id = "files.UserID"'
    sql1 = "SELECT ip, port FROM users WHERE id = %s"
    sql2 = "SELECT UserID From files WHere FileName = %s"

    
    curr.execute(sql2, (fileName, ))

    Userid= curr.fetchone()["userid"]
    
    curr.execute(sql1, (Userid, ))
    
    IPandPort = curr.fetchone()
    ip = IPandPort["ip"]
    port = IPandPort["port"]


    print("/nHere IP", ip)
    print("/nHere port", port)

    result = downloadFile(ip, int(port), fileName, downloadPath)



    # Result is a code
    # 1 = Successful
    # -1 = Error in Connection (Cannot Connect, or Connection Full, or User Is Offline?)
    # -2 = File Wasn't Found (File Owner May Have Moved The File?)
    return result
