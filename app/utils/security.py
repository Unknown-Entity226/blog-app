from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_pass(password: str):
    hash_pass = password_hash.hash(password=password)

    return hash_pass


def verify_pass(password: str, hashed_pass: str):

    return password_hash.verify(password, hashed_pass)
