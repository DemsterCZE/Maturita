import jwt
import os
import dotenv

dotenv.load_dotenv()

key = os.getenv("KEY")

def jwt_decode(token:str) -> any:
    try:
        decoded = jwt.decode(token, key, algorithms=["HS256"])
        return decoded
    except:
        return None