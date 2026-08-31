from pwdlib import PasswordHash

paswword_hash = PasswordHash.recommended()


def hash_pass(password: str) -> str:
    return paswword_hash.hash(password)


def verify_pass(password: str, hashed: str) -> bool:
    return paswword_hash.verify(password, hashed)
