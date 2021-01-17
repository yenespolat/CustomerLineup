from flask import Blueprint, request, render_template, g, redirect, url_for, abort
from flask_login import login_required, current_user
from customer_lineup.utils import LayoutPI
import customer_lineup.workplace.db as wp_db
import customer_lineup.queue_.db as q_db
import requests

workplace_page_bp = Blueprint(
    'workplace_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)


@workplace_page_bp.route('/example')
def example_api():
    # # Example for https://customer-lineup-gr31.herokuapp.com//workplace/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    g.arg0 = request.args.get('arg0')
    g.args = request.args
    return render_template("workplace/example_page.html", page_info=LayoutPI(title="Page title"))

@workplace_page_bp.route('/<int:wp_id>')
def show_workplace(wp_id):
    workplace = requests.get(f'http://127.0.0.1:5000/api/workplace/get_workplace?id={wp_id}').json()
    total_score = 0
    for comment in workplace['comments']:
        total_score += comment['score']
        web_user_id = comment['web_user_ref']
        web_user = requests.get(f'http://127.0.0.1:5000/api/auth/get_user?id={web_user_id}').json()
        comment['web_user_ref'] = web_user['webuser']['name'] + ' ' + web_user['webuser']['surname']
    if total_score == 0:
        avg_score = 'No comments yet'
    else:
        avg_score = total_score / len(workplace['comments'])
    return render_template('workplace.html', workplace=workplace, avg_score=avg_score)

@workplace_page_bp.route('/workplaces')
def all_wps():
    wplaces = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/workplace/get_workplaces').json()
    return render_template('workplaces.html', workplaces=wplaces['workplaces'])

@workplace_page_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 2:
        return redirect(abort(401))
    workplace = wp_db.get_workplace_with_id(current_user.managed_workplace_ref.id)
    queue = q_db.get_users_on_queue_with_workplace(workplace)
    q_today = q_db.get_all_q_today(workplace.id)
    q_alltime = q_db.get_all_q(workplace.id)
    comments = workplace.comments_set
    return render_template('dashboard.html', workplace=workplace, queue=len(queue), q_today=len(q_today), q_alltime=len(q_alltime), comments=len(comments))

@workplace_page_bp.route('/dashboard/edit/<int:wp_id>')
@login_required
def edit_workplace(wp_id):
    workplace = wp_db.get_workplace_with_id(wp_id)
    print(workplace)
    return render_template('edit-workplace.html', workplace=workplace)