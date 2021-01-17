from flask import Blueprint, jsonify, request, g
from passlib.handlers.pbkdf2 import pbkdf2_sha256 as hasher

import customer_lineup.auth.db as db
import customer_lineup.workplace.db as wp_db
from customer_lineup.auth.authorization import application_token_required, web_user_token_required
from customer_lineup.auth.utils import create_web_user_token, decode_token

auth_api_bp = Blueprint('auth_api_bp', __name__)


@auth_api_bp.route("/register", methods=["POST"])
@application_token_required
def register_api():
    form = request.form
    if db.get_webuser_with_email(form["email_address"]) is not None:
        return jsonify(result=False, msg='Email used before!')
    password_hash = hasher.hash(form["password"])
    web_user = db.add_webuser(
        name=form["name"], surname=form["surname"], phone_number=form["phone_number"],
        email=form["email_address"], password_hash=password_hash
    )
    token = create_web_user_token(web_user=web_user)
    return jsonify(result=True, msg='User added!', token=token, web_user=web_user.to_dict())


@auth_api_bp.route("/get_web_user_token", methods=["POST"])
@application_token_required
def get_web_user_token_api():
    form = request.form
    web_user = db.get_webuser_with_email(form["email_address"])
    if not (web_user and hasher.verify(form["password"], web_user.password_hash)):
        return jsonify(result=False, msg='Email or password is incorrect.')
    token = create_web_user_token(web_user=web_user)
    return jsonify(result=True, msg='User added!', token=token, web_user=web_user.to_dict())


@auth_api_bp.route('user_from_token')
@web_user_token_required
def user_from_token_api():
    return jsonify(result=True, web_user=g.web_user.to_dict())


@auth_api_bp.route('/add_user')
def api_add_webuser():
    args = request.args
    if 'email' in args and 'name' in args and 'surname' in args and 'user_type' in args:
        email = args.get('email')
        name = args.get('name')
        surname = args.get('surname')
        user_type = args.get('user_type')
    else:
        return jsonify(result=False, msg='Example usage: /add_user?name=ABC&surname=DEF&email=ghi@jkl.com&user_type=3')

    if db.get_webuser_with_email(email) is not None:
        return jsonify(result=False, msg='Email used before!')

    added_webuser = db.add_webuser(email, name, surname, user_type)
    return jsonify(result=True, msg='User added!', added_webuser=added_webuser.to_dict())


@auth_api_bp.route('/get_user')
def api_get_user():
    args = request.args
    if 'email' in args:
        email = args.get('email')
        webuser = db.get_webuser_with_email(email)
    if 'id' in args:
        user_id = args.get('id')
        webuser = db.get_webuser_with_id(user_id)

    if webuser is None:
        return jsonify(result=False, msg='User not found!')

    return jsonify(result=True, webuser=webuser.to_dict())


@auth_api_bp.route('get_all_users')
def api_get_all_users():
    users = db.get_all_users()
    if users is None:
        return jsonify(result=False, msg='No users registered!')

    user_list = []
    for user in users:
        user_list.append(user.to_dict())

    return jsonify(result=True, users=user_list)

@auth_api_bp.route('edit_user')
def api_edit_webuser():
    args = request.args
    if 'id' in args and 'user_type' in args:
        user_id = args.get('id')
        user_type = args.get('user_type')
        webuser = db.get_webuser_with_id(user_id)
    webuser.user_type = user_type
    return jsonify(result=True, msg='User type changed.')

@auth_api_bp.route('/assign_user_to_wp')
def api_assign_user_to_wp():
    args = request.args
    if 'user_id' in args and 'workplace_id' in args:
        user_id = args.get('user_id')
        workplace_id = args.get('workplace_id')
    else:
        return jsonify(result=False, msg='Example usage: /api_assign_user_to_wp?user_id=1&workplace_id=2')

    webuser = db.get_webuser_with_id(user_id)
    if webuser.user_type != 2 or webuser.managed_workplace_ref is not None:
        return jsonify(result=False, msg='Given user is not wp manager or assigned before!')

    workplace = wp_db.get_workplace_with_id(workplace_id)
    db.asign_user_to_workplace(webuser, workplace)
    return jsonify(result=True, user=webuser.name + ' ' + webuser.surname, workplace=workplace.name,
                   msg='User assigned to workplace as manager.')
