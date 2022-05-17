#!/usr/bin/env python3
"""
Module basic_auth
"""
from base64 import b64decode
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        returns the Base64 part of the
        Authorization header for a Basic Authentication
        """
        if authorization_header and isinstance(
                authorization_header,
                str) and authorization_header.startswith("Basic "):
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string
        """
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                return b64decode(
                    base64_authorization_header).decode('utf-8')
            except Exception:
                return None
