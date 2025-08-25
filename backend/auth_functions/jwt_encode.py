import jwt
import dotenv
import os

dotenv.load_dotenv

key = os.getenv("KEY")

def jwt_encode(login : str , roleID : int) -> str:
    encoded = jwt.encode({"username": login,"RoleID": roleID}, key, algorithm="HS256")
    return encoded