import psycopg2
import db_connection as db

#PLEASE call update_description(userID, newDescription) in edit Method of ShareFileMethods
#in def editShareFileDescription(userID, fileName, newDescription): update_description(userID, newDescription)
#also in ShareFileMethods.py make sure to write the import ---> from update_description import update_description
def update_description(userID, newDescription):
    try:
        conn = db.connectDataBase()
        if conn is None:
            print("Failed to connect to the database.")
            return False

        cur = conn.cursor()
        update_sql = "UPDATE \"files\" SET Description = %s WHERE userID = %s"
        cur.execute(update_sql, (newDescription, userID))
        conn.commit()
        print("Updated Description!")
        return True
    except psycopg2.Error as e:
        print("Could not update Description:", e)
        return False
    finally:
        if conn is not None:
            conn.close()

            
            