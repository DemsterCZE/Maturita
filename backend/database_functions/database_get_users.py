from .connection_init import get_connection
import mysql.connector

def database_get_users() -> list | dict:
    database = get_connection()
    cursor = database.cursor(dictionary=True)
    try:
        cursor.execute(
        """ SELECT id,username,highest_score FROM users WHERE roleID <> 1 ORDER BY highest_score DESC"""
        )
        users = cursor.fetchall()
    except(mysql.connector.Error):
        cursor.close()
        database.close()
        return {"Error" : "Něco se pokazilo"}
    cursor.close()
    database.close()
    return users