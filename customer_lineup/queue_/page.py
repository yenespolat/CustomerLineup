from flask import Blueprint, request, render_template, g
from flask_login import current_user
from customer_lineup.utils import LayoutPI
from customer_lineup.utils.global_vars import global_url_prefix
import requests, json
from datetime import datetime

queue_page_bp = Blueprint(
    'queue_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)

@queue_page_bp.route('/queue-history')
def queue_hist():
    if current_user.is_authenticated: #if current_user
        userid = current_user.id
        queues = requests.get(f'{global_url_prefix}/api/queue/user_history?id={userid}').json()['queue_list']
        for queue in queues:
            wp_id = queue['workplaces_ref']
            wp = requests.get(f'{global_url_prefix}/api/workplace/get_workplace?id={wp_id}').json()
            queue['workplaces_ref'] = wp['name'] + ' ' + wp['district'] + ' ' + str(wp['id'])
            date_time_obj = datetime.strptime(queue['status_time'], '%Y-%m-%dT%H:%M:%S.%f')
            date_time_str = date_time_obj.strftime("%m/%d/%Y %H:%M")
            queue['status_time'] = date_time_str
            if queue['comment_ref']:
                comment_id = queue['comment_ref']
                comment = requests.get(f'{global_url_prefix}/api/comment/get_comment?id={comment_id}').json()
                queue['comment_ref'] = comment
    return render_template('queue-history.html', queues=queues)

