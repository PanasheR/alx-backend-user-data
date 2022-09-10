#!/usr/bin/env python3
"""
Main Flask app file
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Register_user func
    """
    req = requests.post('http://0.0.0.0:5000/users',
                        {'email': email, 'password': password})
    assert req.status_code == 200
    assert req.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Log_in_wrong_password func
    """
    req = requests.post('http://0.0.0.0:5000/sessions',
                        {'email': email, 'password': password})
    assert req.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    Log_in func
    """
    req = requests.post('http://0.0.0.0:5000/sessions',
                        {'email': email, 'password': password})
    assert req.status_code == 200
    assert req.json() == {"email": email, "message": "logged in"}
    return req.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Profile_unlogged func
    """
    req = requests.get('http://0.0.0.0:5000/profile')
    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    Profile_logged func
    """
    req = requests.get('http://0.0.0.0:5000/profile',
                       cookies={'session_id': session_id})
    assert req.status_code == 200
    assert req.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """
    Log_out func
    """
    req = requests.delete('http://0.0.0.0:5000/sessions',
                          cookies={'session_id': session_id})
    assert req.status_code == 200
    assert req.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """
    Reset_password_token func
    """
    req = requests.post('http://0.0.0.0:5000/reset_password',
                        {'email': email})
    assert req.status_code == 200
    return req.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update_password func
    """
    req = requests.put('http://0.0.0.0:5000/reset_password',
                       {'email': email, 'reset_token': reset_token,
                        'new_password': new_password})
    assert req.status_code == 200
    assert req.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
