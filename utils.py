import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_hashed_password):
    return hash_password(input_password) == stored_hashed_password
