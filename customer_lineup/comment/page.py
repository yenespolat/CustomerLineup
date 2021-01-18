from flask import Blueprint, request, render_template, g, redirect, url_for
from flask_login import current_user
from customer_lineup.utils import LayoutPI
from customer_lineup.utils.global_vars import global_url_prefix
import customer_lineup.comment.db as db_comment
import customer_lineup.auth.db as db_auth
import customer_lineup.queue_.db as q_db
import customer_lineup.workplace.db as wp_db
import requests

comment_page_bp = Blueprint(
    'comment_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)


@comment_page_bp.route('/comment/<int:q_id>', methods=['GET', 'POST'])
def comment(q_id):
    if request.method == 'POST':
        score = request.form['score']
        comment = request.form['comment']
        added_comment = requests.get(f'{global_url_prefix}/api/comment/add_comment?queue_id={q_id}&score={score}&comment={comment}')
        print(score, comment, added_comment.text, 'sdfasdf')
        return redirect(url_for('queue_page_bp.queue_hist'))
    q_elm = requests.get(f'{global_url_prefix}/api/queue/get_q?id={q_id}').json()['queue_element']
    wp_id = q_elm['workplaces_ref']
    wp = requests.get(f'{global_url_prefix}/api/workplace/get_workplace?id={wp_id}').json()
    q_elm['workplaces_ref'] = wp['name'] + ' ' + wp['district'] + ' ' + str(wp['id'])
    return render_template('comment.html', queue_ref=q_elm)
