from auth_functions.jwt_decode import jwt_decode
from .connection_init import get_connection
import mysql.connector

def update_score(token: str,score : int) -> bool:
    token = token.split(" ",1)[1]
    login = jwt_decode(token=token)["username"]
    database = get_connection()
    
    try:
        cursor = database.cursor()
        cursor.execute("""
        UPDATE userss
        SET highest_score=%s
        WHERE username=%s OR email=%s
""",(score,login,login,))
        database.commit()
        cursor.close()
        database.close()
        return True
        
    except mysql.connector.Error as e:
        
        return False