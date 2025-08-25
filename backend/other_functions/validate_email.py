import re

email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def validate_email(email : str) -> bool:
    if re.match(email_regex, email):
        return True 
    else:
        return False