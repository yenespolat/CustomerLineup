from flask import Blueprint, jsonify, request

queue_api_bp = Blueprint('queue_api_bp', __name__)


@queue_api_bp.route('/example')
def example_api():
    # Example for http://127.0.0.1:5000/api/queue/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    arg0 = request.args.get('arg0')
    return jsonify(result=True, msg="Hello world", data=arg0)
