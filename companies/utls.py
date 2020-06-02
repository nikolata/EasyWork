import hashlib


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()
