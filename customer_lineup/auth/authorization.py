from functools import wraps

from flask import request, jsonify, g

from customer_lineup.auth import db
from customer_lineup.auth.utils import decode_token


def web_user_token_required(func):
    @wraps(func)
    @application_token_required
    def decorated_view(*args, **kwargs):
        web_user_token = request.headers.get("web_user_token")
        if not web_user_token:
            return jsonify(result=False, msg="Web user token is not send", token_error=3)
        elif not decode_token(web_user_token):
            return jsonify(result=False, msg="Web user token is not valid", token_error=4)
        elif not db.get_webuser_with_id(id=decode_token(web_user_token)["web_user_id"]):
            return jsonify(result=False, msg="Web user not found.", token_error=5)
        g.web_user = db.get_webuser_with_id(id=decode_token(web_user_token)["web_user_id"])
        return func(*args, **kwargs)

    return decorated_view


def application_token_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        application_token = request.headers.get("application_token")
        if not application_token:
            return jsonify(result=False, msg="Application token is not send", token_error=1)
        elif not decode_token(application_token):
            return jsonify(result=False, msg="Application token is not valid", token_error=2)
        return func(*args, **kwargs)

    return decorated_view
