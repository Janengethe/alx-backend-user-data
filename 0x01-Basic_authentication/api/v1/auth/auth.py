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
        """
        returns True if the path is not in the list of strings excluded_paths
        """
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path) or path.startswith(i):
                    return False
                if i[-1] == "*" and path.startswith(i[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """returns authorization"""
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns none"""
        return None
