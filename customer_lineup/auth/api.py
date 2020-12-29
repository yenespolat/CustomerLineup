from flask import Blueprint, jsonify, request
import customer_lineup.auth.db as db
import customer_lineup.workplace.db as wp_db

auth_api_bp = Blueprint('auth_api_bp', __name__)


@auth_api_bp.route('/example')
def example_api():
    # Example for http://127.0.0.1:5000/api/auth/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    arg0 = request.args.get('arg0')
    return jsonify(result=True, msg="Hello world", data=arg0)

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
    return jsonify(result=True, user=webuser.name + ' ' + webuser.surname, workplace=workplace.name, msg='User assigned to workplace as manager.')
