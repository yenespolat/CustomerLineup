from flask import Blueprint, request, render_template, g
from customer_lineup.utils import LayoutPI
import requests, json
from datetime import datetime

queue_page_bp = Blueprint(
    'queue_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)


@queue_page_bp.route('/example')
def example_api():
    # # Example for http://127.0.0.1:5000/queue/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    g.arg0 = request.args.get('arg0')
    g.args = request.args
    return render_template("queue_/example_page.html", page_info=LayoutPI(title="Page title"))

@queue_page_bp.route('/queue-history')
def queue_hist():
    if True: #if current_user
        userid = 1
        queues = requests.get(f'http://127.0.0.1:5000/api/queue/user_history?id={userid}').json()['queue_list']
        for queue in queues:
            wp_id = queue['workplaces_ref']
            wp = requests.get(f'http://127.0.0.1:5000/api/workplace/get_workplace?id={wp_id}').json()
            queue['workplaces_ref'] = wp['name'] + ' ' + wp['district'] + ' ' + str(wp['id'])
            date_time_obj = datetime.strptime(queue['status_time'], '%Y-%m-%dT%H:%M:%S.%f')
            date_time_str = date_time_obj.strftime("%m/%d/%Y %H:%M")
            queue['status_time'] = date_time_str
            if queue['comment_ref']:
                comment_id = queue['comment_ref']
                comment = requests.get(f'http://127.0.0.1:5000/api/comment/get_comment?id={comment_id}').json()
                queue['comment_ref'] = comment
            print(queue['comment_ref']['comment']['score'])
    return render_template('queue-history.html', queues=queues)

