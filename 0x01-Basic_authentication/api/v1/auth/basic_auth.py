#!/usr/bin/env python3
"""
Basic Auth module
"""

import base64
from api.v1.auth.auth import Auth


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
