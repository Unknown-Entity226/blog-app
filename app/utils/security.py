from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_pass(password: str):
    hash_pass = password_hash.hash(password=password)

    return hash_pass



