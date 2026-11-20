from sqlalchemy import select
from sqlalchemy.orm import Session

from auth_system.utils.hash import PasswordHasher

from .user_models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._password_hasher = PasswordHasher()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self._session.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self._session.scalar(statement)

    def register(
        self,
        email: str,
        username: str,
        password: str,
    ) -> User | None:
        if (self.get_by_email(email) is not None
            or self.get_by_username(username) is not None
        ):
            return None

        user = User(
            email=email,
            username=username,
            password=self._password_hasher.hash_password(password),
        )
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

        return user

    def authenticate(self, email: str, password: str) -> User | None:
        user = self.get_by_email(email)

        if user is None:
            return None

        if not self._password_hasher.check_password(password, user.password):
            return None

        return user
