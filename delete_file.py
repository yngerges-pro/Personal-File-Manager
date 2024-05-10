import psycopg2
import db_connection as db

#PLEASE call delete_file(userID, fileName) in delete Method of ShareFileMethods
#in def deleteShareFile(userID, fileName, Path): delete_file
#also in ShareFileMethods.py make sure to write the import ---> from delete_file import delete_file
def delete_file(userID, fileName):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        delete_sql = "DELETE FROM files WHERE userID = %s AND FileName = %s"
        cur.execute(delete_sql, (userID, fileName))
        conn.commit()
        print("Deleted file!")
        return True
    except psycopg2.Error as e:
        print("Could not delet file:", e)
        return False
    finally:
        if conn is not None:
            conn.close()
