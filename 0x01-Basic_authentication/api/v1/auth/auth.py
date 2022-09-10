#!/usr/bin/env python3
'''
managing API authentification
'''
from flask import request
from typing import TypeVar, List


class Auth():
    '''
    managing the API authentification
    '''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        ''' require_auth func '''
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if path is None or excluded_paths is None:
            return True
        path = path + '/' if path[-1] != '/' else path
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        ''' authorization_header func '''
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        ''' current_user func '''
        return None
