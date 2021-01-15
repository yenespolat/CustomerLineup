from flask import Blueprint, request, render_template, g
from customer_lineup.utils import LayoutPI
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
    workplace = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/workplace/get_workplace?id={wp_id}').json()
    total_score = 0
    for comment in workplace['comments']:
        total_score += comment['score']
        web_user_id = comment['web_user_ref']
        web_user = requests.get(f'https://customer-lineup-gr31.herokuapp.com//api/auth/get_user?id={web_user_id}').json()
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
def dashboard():
    return render_template('dashboard.html')
