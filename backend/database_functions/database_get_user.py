from .connection_init import get_connection
import mysql.connector
from auth_functions.jwt_decode import jwt_decode


def database_get_user(token:str)-> list | dict:
    database = get_connection()
    cursor = database.cursor(dictionary=True) 
    token = token.split(" ",1)[1]
    decoded_token = jwt_decode(token=token)
    try:
        cursor.execute("""
        SELECT roleID,username,highest_score FROM users WHERE username=%s
        """,(decoded_token['username'],))
        user = cursor.fetchall()
        
    except(mysql.connector.Error):
        cursor.close()
        database.close()
        return {"Error" : "Něco se pokazilo"}
    if user ==[]:
        cursor.close()
        database.close()
        return({"Error":"Uživatel neexistuje"})  
    cursor.close()
    database.close()   
    return user