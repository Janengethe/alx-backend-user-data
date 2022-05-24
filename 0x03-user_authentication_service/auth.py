#!/usr/bin/env python3
"""
Module auth
"""
import bcrypt
from user import User
from sqlalchemy.exc import NoResultFound

from db import DB


def _hash_password(password: str) -> bytes:
    """
    returned bytes is a salted hash of the input password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialization"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")
