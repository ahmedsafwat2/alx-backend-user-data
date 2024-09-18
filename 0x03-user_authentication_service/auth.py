#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user
        """
        db = self._db
        try:
            db.find_user_by(email=email)
        except NoResultFound:
            user = db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """valid_login
        """
        db = self._db
        try:
            user = db.find_user_by(email=email)
            plain_password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(plain_password_bytes, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates_session
        """


def _hash_password(password: str) -> bytes:
    """_hash_password
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd


def _generate_uuid() -> str:
    """_generate_uuid
    """
    return str(uuid4())
