import hashlib


def hash_password(password):
    """
    Hash a password for storing, using SHA256.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def check_password_hash(password, hashed_password):
    """
    Check that a password matches a stored hash.
    """
    return hash_password(password) == hashed_password
