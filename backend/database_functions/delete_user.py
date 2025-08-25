from .connection_init import get_connection
import mysql.connector

def database_delete_user(id):
    database = get_connection()
    cursor = database.cursor(dictionary=True)
    try:
        cursor.execute(
            """DELETE FROM users WHERE id = %s""",(id,)
        )
    except mysql.connector.Error:
        cursor.close()
        database.close()
        return 
    database.commit()
    cursor.close()
    database.close()
    return 