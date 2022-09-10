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
        '''self descriptive'''
        if not path or not excluded_paths:
            return True

        path += '/' if path[-1] != '/' else ''
        wildcard = any(rex.endswith("*") for rex in excluded_paths)

        if not wildcard:
            if path in excluded_paths:
                return False

        for rex in excluded_paths:
            if rex[-1] == '*':
                if path.startswith(rex[:-1]):
                    return False
            if rex == path:
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
