from flask import Blueprint, jsonify, request
import customer_lineup.queue_.db as db
import customer_lineup.auth.db as auth_db
import customer_lineup.workplace.db as wp_db

queue_api_bp = Blueprint('queue_api_bp', __name__)


@queue_api_bp.route('/enqueue')
def api_enqueue():  #status'a gerek yok, çünkü direk 1 olarak ekleniyor
    args = request.args
    if 'user_id' in args and 'workplace_id' in args and 'type' in args and 'waiting_person' in args:
        user_id = args.get('user_id')
        workplace_id = args.get('workplace_id')
        type = args.get('type')
        waiting_person = args.get('waiting_person')
    else:
        return jsonify(result=False, msg='Example usage: /enqueue?user_id=1&workplace_id=2&type=1&waiting_person=1')

    user = auth_db.get_webuser_with_id(user_id)
    if db.get_active_queue(user) is not None:
        return jsonify(result=False, msg='User already in another queue_!')

    workplace = wp_db.get_workplace_with_id(workplace_id)
    enqueued = db.add_queue_element(user, workplace, 1, type, waiting_person)

    return jsonify(result=True, msg='User enqueued.', enqueued=enqueued.to_dict())

@queue_api_bp.route('/dequeue')
def api_dequeue():
    args = request.args
    if 'status' in args and 'queue_id' in args:
        queue_id = args.get('queue_id')
        status = args.get('status')
        queue = db.get_queue_with_id(queue_id)
    elif 'status' in args and 'user_id' in args:
        user_id = args.get('user_id')
        status = args.get('status')
        queue = db.get_active_queue(user_id)
    else:
        return jsonify(result=False, msg='Example usage: /dequeue?queue_id=1&status=3 or \n /change_status?user_id=1&status=2')

    if queue is None:
        return jsonify(result=False, msg='User not in queue_!')

    db.change_queue_status(queue.id, status)
    return jsonify(result=True, msg='Status changed.', queue=queue.to_dict())

@queue_api_bp.route('/user_history')
def api_user_history():
    args = request.args
    if 'id' in args:
        user_id = args.get('id')
    else:
        return jsonify(result=False, msg='Example usage: /user_history?id=1')

    user = auth_db.get_webuser_with_id(user_id)
    queues = db.get_all_user_queues(user)
    queue_list = []
    for queue in queues:
        queue_list.append(queue.to_dict())

    return jsonify(result=True, queue_list=queue_list, user=user.to_dict())

@queue_api_bp.route('workplace_queue')
def api_workplace_queue():
    args = request.args
    if 'id' in args:
        workplace_id = args.get('id')
    else:
        return jsonify(result=False, msg='Example usage: /workplace_queue?id=1')

    workplace = wp_db.get_workplace_with_id(workplace_id)
    waiting_users = db.get_users_on_queue_with_workplace(workplace)

    user_list = []
    for user in waiting_users:
        user_list.append(user.to_dict())

    return jsonify(result=True, user_list=user_list, workplace=workplace.to_dict())