#!/usr/bin/env python3
"""
Basic Auth module
"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    class BasicAuth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """base64 authorization
        """
        if (authorization_header is None or
                not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic ")):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """base64decode
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            dc_bytes = base64.b64decode(base64_authorization_header)
            dc_str = dc_bytes.decode('utf-8')
            return dc_str
        except(base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extract credentials
        """
        dbah = decoded_base64_authorization_header
        if dbah is None or not isinstance(dbah, str):
            return (None, None)
        if ':' not in dbah:
            return (None, None)
        parts = dbah.split(':')
        return tuple(parts)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """Retrieves a user based on the user's authentication credentials.
        """
        if user_email is None:
            return None
        if user_pwd is None:
            return None
        if type(user_email) != str or type(user_pwd) != str:
            return None
        users = User.search({"email": user_email})
        if len(users) <= 0:
            return None
        if users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        auth_body = self.authorization_header(request)
        dbah = self.extract_base64_authorization_header(auth_body)
        upd = self.decode_base64_authorization_header(dbah)
        un, up = self.extract_user_credentials(upd)
        return self.user_object_from_credentials(un, up)
