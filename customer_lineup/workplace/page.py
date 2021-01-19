from flask import Blueprint, request, render_template, g, redirect, url_for, abort
from flask_login import login_required, current_user
from customer_lineup.utils import LayoutPI
from customer_lineup.utils.global_vars import global_url_prefix
import customer_lineup.workplace.db as wp_db
import customer_lineup.queue_.db as q_db
import requests

workplace_page_bp = Blueprint(
    'workplace_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)

@workplace_page_bp.route('/<int:wp_id>')
def show_workplace(wp_id):
    workplace = requests.get(f'{global_url_prefix}/api/workplace/get_workplace?id={wp_id}').json()
    total_score = 0
    for comment in workplace['comments']:
        total_score += comment['score']
        web_user_id = comment['web_user_ref']
        web_user = requests.get(f'{global_url_prefix}/api/auth/get_user?id={web_user_id}').json()
        comment['web_user_ref'] = web_user['webuser']['name'] + ' ' + web_user['webuser']['surname']
    if total_score == 0:
        avg_score = 'No comments yet'
    else:
        avg_score = total_score / len(workplace['comments'])
    return render_template('workplace.html', workplace=workplace, avg_score=avg_score)

@workplace_page_bp.route('/workplaces')
def all_wps():
    wplaces = requests.get(f'{global_url_prefix}/api/workplace/get_workplaces').json()
    return render_template('workplaces.html', workplaces=wplaces['workplaces'])

@workplace_page_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type != 2 or current_user.managed_workplace_ref is None:
        return redirect(abort(401))
    workplace = wp_db.get_workplace_with_id(current_user.managed_workplace_ref.id)
    q_now = q_db.get_users_on_queue_with_workplace(workplace)
    q_today = q_db.get_all_q_today(workplace.id)
    q_alltime = q_db.get_all_q(workplace.id)
    comments = workplace.comments_set
    return render_template('dashboard.html', workplace=workplace, q_now=len(q_now), q_today=len(q_today), q_alltime=len(q_alltime), comments=len(comments))

@workplace_page_bp.route('/dashboard/edit/<int:wp_id>', methods=['GET', 'POST'])
@login_required
def edit_workplace(wp_id):
    workplace = wp_db.get_workplace_with_id(wp_id)
    if request.method == 'POST':
        new_name = request.form['name']
        new_type = request.form['type']
        new_wlimit = request.form['warnlimit']
        workplace.set(name = new_name)
        workplace.set(type = new_type)
        if len(new_wlimit) > 0:
            workplace.set(staff_warning_limit=int(new_wlimit))
        return redirect(url_for('workplace_page_bp.dashboard'))
    return render_template('edit-workplace.html', workplace=workplace)

@workplace_page_bp.route('/delete/<int:wp_id>')
@login_required
def delete_workplace(wp_id):
    wp_db.delete_wp(wp_id)
    return redirect(url_for('admin_page_bp.manage_workplacespage'))