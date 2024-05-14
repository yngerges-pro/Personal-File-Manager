# Methods used for the Download Files Screen
import db_connection as db
from ReceivingSide import *

def viewAllDownloadableFiles():
    conn = db.connectDataBase()
    curr = conn.cursor()

    # Need to join files table and users tables, only return where
    # Status = true in usersip
    sql = 'SELECT "FileName", "FileSize", "Description" FROM files JOIN users ON users.status = true'

    result = curr.execute(sql)

    conn.close()
    curr.close()

    # result is a list
    return result

def searchForDownloadableFiles(searchWith):
    conn = db.connectDataBase()
    curr = conn.cursor()

    searchWith = "%" + searchWith + "%" # Add wild cards front and back of searching with
    sql = "SELECT f.FileName, f.FileSize, f.Description FROM files JOIN users ON u.status = true AND fileName = " + searchWith

    result = curr.execute(sql)

    conn.close()
    curr.close()
    # Need to join files table and usersip table together, only return where
    # Status = true AND LIKE fileName = searchWith
    # result is a list
    return result

def downloadThisFile (fileName, downloadPath):
    # SQL query usersip table, grab IP and Port
    conn = db.connectDataBase()
    curr = conn.cursor()

    sql = "SELECT ip, port FROM users"
    info = curr.execute(sql)
    print(info)
    ip = ""
    port = 0000

    # result = downloadFile(ip, port, fileName, downloadPath)

    # Result is a code
    # 1 = Successful
    # -1 = Error in Connection (Cannot Connect, or Connection Full, or User Is Offline?)
    # -2 = File Wasn't Found (File Owner May Have Moved The File?)
    return info
