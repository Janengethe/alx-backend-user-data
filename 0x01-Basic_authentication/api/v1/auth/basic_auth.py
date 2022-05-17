#!/usr/bin/env python3
"""
Module basic_auth
"""
from base64 import b64decode
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header,
                str) and ":" in decoded_base64_authorization_header:
            email, psswd = decoded_base64_authorization_header.split(":", 1)
            return email, psswd
        return(None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(b64_header)
        user_creds = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(*user_creds)
