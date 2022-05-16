#!/usr/bin/env python3
"""
Module auth
"""
from typing import List, TypeVar
from flask import request


class Auth():
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """To work on it later"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns none"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
