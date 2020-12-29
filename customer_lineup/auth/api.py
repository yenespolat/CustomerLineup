from flask import Blueprint, jsonify, request

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