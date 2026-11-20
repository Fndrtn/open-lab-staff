from pwdlib import PasswordHash


class PasswordHasher:
    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash_password(self, password: str) -> str:
        return self._password_hash.hash(password)

    def check_password(
            self,
            password: str,
            hashed_password: str,
    ) -> bool:
        return self._password_hash.verify(password, hashed_password)