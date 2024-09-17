#!/usr/bin/env python3
"""
Authentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """_hash_password
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pwd
