from datetime import datetime

import jwt as jwt
from flask import current_app
from jwt import InvalidSignatureError, DecodeError
from pony.orm import flush

from customer_lineup.utils.db_models import WebUser


def create_web_user_token(web_user: WebUser):
    if not web_user.id:
        flush()

    data = {
        'web_user_id': web_user.id,
        'email_address': web_user.email_address,
        'created_time': datetime.now()
    }
    return jwt.encode(
        data, current_app.secret_key, algorithm='HS256', json_encoder=current_app.json_encoder
    )


def decode_token(token):
    try:
        return jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
    except (InvalidSignatureError, DecodeError):
        return None


def form_validation_errors_for_register(name, surname, email, password, password_verification):
    err_list = []
    return err_list


def form_validation_errors_for_login(email, password):
    err_list = []
    return err_list
