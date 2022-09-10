#!/usr/bin/env python3
'''Session Auth class'''

from api.v1.auth.auth import Auth
from flask import request
from models.user import User
from typing import List, TypeVar
import base64
import uuid


class SessionAuth(Auth):
    '''  self auth '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' create_session def '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' user_id_for_session_id '''
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        ''' current_user '''
        session_cookie = self.session_cookie(request)
        session_id = self.user_id_for_session_id(session_cookie)
        return User.get(session_id)

    def destroy_session(self, request=None):
        ''' destroy_session '''
        if not request:
            return False
        session_cookie = self.session_cookie(request)

        if not session_cookie:
            return False

        user_id = self.user_id_for_session_id(session_cookie)

        if not user_id:
            return False
        self.user_id_by_session_id.pop(session_cookie)
        return True
