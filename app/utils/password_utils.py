
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError


class PasswordManager:

    def __init__(self):
        self._hasher = PasswordHasher()

    def hash_password(self, password: str) -> str:

        return self._hasher.hash(password)

    def verify_password(
        self,
        password: str,
        hashed_password: str
    ) -> bool:

        try:
            return self._hasher.verify(
                hashed_password,
                password
            )

        except VerificationError:
            return False


password_manager = PasswordManager()
