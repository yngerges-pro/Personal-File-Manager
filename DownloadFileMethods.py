import psycopg2
from ReceivingSide import *

def viewAllDownloadableFiles(cursorObject):
    sql = ""
    # Need to join files table and usersip table together, only return where
    # Status = true in usersip

    # Could just call the search method where search by ""

    # result is a list
    return result

def searchForDownloadableFiles(searchWith, cursorObject):
    searchWith = "%" + searchWith + "%" # Add wild cards front and back of searching with
    sql = ""

    # Need to join files table and usersip table together, only return where
    # Status = true AND LIKE fileName = searchWith

    # result is a list
    return result

def downloadThisFile (fileOwnerID, fileName, Path, cursorObject):
    sql = ""
    # SQL query usersip table, grab IP and Port

    # Could join usersip and files, and grab IP and Port using fileName

    Ip = ""
    Port = 0000

    result = downloadFile(Ip, Port, fileName, Path)

    # Result is a code
    # 1 = Successful
    # -1 = Error in Connection (Cannot Connect, or Connection Full, or User Is Offline?)
    # -2 = File Wasn't Found (File Owner May Have Moved The File?)
    return result
