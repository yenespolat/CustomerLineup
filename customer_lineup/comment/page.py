from flask import Blueprint, request, render_template, g, redirect, url_for
from customer_lineup.utils import LayoutPI
import requests

comment_page_bp = Blueprint(
    'comment_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)


@comment_page_bp.route('/example')
def example_api():
    # # Example for https://customer-lineup-gr31.herokuapp.com//comment/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    g.arg0 = request.args.get('arg0')
    g.args = request.args
    return render_template("comment/example_page.html", page_info=LayoutPI(title="Page title"))

@comment_page_bp.route('/comment/<int:q_id>', methods=['GET', 'POST'])
def comment(q_id):
    if request.method == 'POST':
        score = request.form['score']
        comment = request.form['comment']
        added_comment = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/comment/add_comment?queue_id={q_id}&score={score}&comment={comment}')
        return redirect(url_for('queue_page_bp.queue_hist'))
    q_elm = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/queue/get_q?id={q_id}').json()['queue_element']
    wp_id = q_elm['workplaces_ref']
    wp = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/workplace/get_workplace?id={wp_id}').json()
    q_elm['workplaces_ref'] = wp['name'] + ' ' + wp['district'] + ' ' + str(wp['id'])
    return render_template('comment.html', queue_ref=q_elm)
