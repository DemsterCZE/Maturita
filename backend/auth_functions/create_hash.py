import argon2

def create_hash(passwd : str) -> str:
    hash_builder : argon2.PasswordHasher = argon2.PasswordHasher(salt_len=8,hash_len=24)
    hashed_password : str = hash_builder.hash(passwd)
    return hashed_password
