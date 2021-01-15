from flask import Blueprint, jsonify, request
import customer_lineup.comment.db as db
import customer_lineup.workplace.db as wp_db
import customer_lineup.auth.db as auth_db
import customer_lineup.queue_.db as q_db
import requests

comment_api_bp = Blueprint('comment_api_bp', __name__)


@comment_api_bp.route('/add_comment')
def api_add_comment():
    args = request.args
    if 'workplace_id' in args and 'user_id' in args and 'score' in args:
        wp_id = args.get('workplace_id')
        user_id = args.get('user_id')
        score = args.get('score')
        workplace = wp_db.get_workplace_with_id(wp_id)
        user = auth_db.get_webuser_with_id(user_id)
        added_comment = db.add_comment_wo_qelement(user, workplace, score, 'No comment')
    elif 'queue_id' in args and 'score' in args:
        q_id = args.get('queue_id')
        q_elm = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/queue/get_q?id={q_id}').json()['queue_element']
        wp_id = q_elm['workplaces_ref']
        user_id = q_elm['web_users_ref']
        score = args.get('score')
        workplace = wp_db.get_workplace_with_id(wp_id)
        queue_element = q_db.get_queue_with_id(q_id)
        user = auth_db.get_webuser_with_id(user_id)
        added_comment = db.add_comment_with_qelement(user, workplace, score, 'No comment', queue_element)
    else:
        return jsonify(result=False, msg='Example usage: /add_comment?workplace_id=1&user_id=1&score=5 or \n /add_comment?workplace_id=1&user_id=1&score=5&comment=XYZ')

    if 'comment' in args:
        comment = args.get('comment')
        added_comment.comment = comment
    return jsonify(result=True, added_comment=added_comment.to_dict())

@comment_api_bp.route('/delete_comment')
def api_delete_comment():
    args = request.args
    if 'id' in args:
        id = args.get('id')
    else:
        return jsonify(result=False, msg='Example usage: /delete_comment?id=1')

    if db.get_comment(id) is None:
        return jsonify(result=False, msg='Comment not found!')

    deleted_comment = db.get_comment(id).to_dict()
    db.delete_comment(id)
    return jsonify(result=True, msg='Comment deleted!', deleted_comment=deleted_comment)

@comment_api_bp.route('/get_comment')
def api_get_comment():
    args = request.args
    if 'id' in args:
        id = args.get('id')
    else:
        return jsonify(result=False, msg='Example usage: /get_comment?id=1')

    if db.get_comment(id) is None:
        return jsonify(result=False, msg='Comment not found!')

    comment = db.get_comment(id).to_dict()
    return jsonify(result=True, msg='Comment deleted!', comment=comment)
