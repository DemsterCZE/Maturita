from .connection_init import get_connection
import mysql.connector

def add_user(username: str, email: str, password_hash: str) -> dict:
    database = get_connection()
    try:
        cursor = database.cursor()
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, RoleID)
            VALUES (%s, %s, %s, 2)
            """,
            (username, email, password_hash)
        )
        database.commit()
        cursor.close()
        database.close()
        
        return {"Success": "Uživatel registrován"}
    except mysql.connector.Error as e:
        
        return {"Error": "Problém s databází"}