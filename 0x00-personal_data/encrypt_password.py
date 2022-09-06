#!/usr/bin/env python3
"""
Password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Passwords encrypting """
    pas = password.encode()
    return bcrypt.hashpw(pas, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check that password provided matches hashed password """
    return bcrypt.checkpw(password.encode(), hashed_password)
