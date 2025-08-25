from database_functions.connection_init import get_connection
from .jwt_encode import jwt_encode
from .jwt_decode import jwt_decode
import argon2

def authentication(login : str, password : str) -> dict:
    database = get_connection()
    cursor = database.cursor()
    try:
        cursor.execute(""" SELECT password_hash FROM users WHERE username=%s OR email=%s LIMIT 1""" ,(login,login))
        database_password = cursor.fetchone()
        authenticator = argon2.PasswordHasher()
        if database_password:
            authenticator.verify(hash=database_password[0],password=password)
            cursor.execute('''
            SELECT users.username, roles.RoleID
            FROM users
            INNER JOIN roles ON users.RoleID = roles.RoleID
            WHERE users.username=%s OR users.email=%s
            ''',(login,login))
            data = cursor.fetchone()
            username = data[0]
            role = data[1]
            token = jwt_encode(login=username,roleID=role)
            decoded_token = jwt_decode(token)
            cursor.close()
            database.close()
            return {"Success" : f"Uživatel {decoded_token['username']} úspěšně přihlášen",
            "Token" : token
            }
              
        else:
            cursor.close()
            database.close()
            return {"Error" : "špatné jméno nebo heslo"}

    except argon2.exceptions.VerifyMismatchError as e:
        cursor.close()
        database.close()
        return {"Error" : "špatné jméno nebo heslo"}