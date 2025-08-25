from .jwt_decode import jwt_decode

def token_in_header_check(token : str) -> bool:
    if token != None:
        token = token.split(" ",1)[1]
        if jwt_decode(token):
            return True
        else:
            return False