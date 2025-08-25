from .connection_init import get_connection
import mysql.connector

def check_for_username_availability(username : str, email : str) -> bool | dict:
    database = get_connection()
    cursor = database.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = %s OR email  = %s", (username,email,))
        result = cursor.fetchone()
        
        if result[0] > 0:
            cursor.close()
            database.close()
            return False  
        else:
            cursor.close()
            database.close()
            return True 

    except mysql.connector.Error as e:
        
        return {"Error" : "Problém s databází"}