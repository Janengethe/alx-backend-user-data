#!/usr/bin/env python3
"""
Module encrypt_password
"""
import bcrypt


def hash_password(password):
    """
    Returns a salted, hashed password, which is a byte string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
