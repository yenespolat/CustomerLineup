from flask import Blueprint, request, render_template, g, flash, redirect, url_for
from flask_login import login_user
from passlib.hash import pbkdf2_sha256 as hasher

from customer_lineup.auth import db
from customer_lineup.auth.utils import form_validation_errors_for_register, form_validation_errors_for_login
from customer_lineup.utils import LayoutPI
from customer_lineup.utils.db_models import WebUser

auth_page_bp = Blueprint(
    'auth_page_bp', __name__,
    template_folder='templates', static_folder='static', static_url_path='assets'
)


@auth_page_bp.route('/example')
def example_api():
    # # Example for http://127.0.0.1:5000/auth/example?arg0=55&arg1=asd&arg1=qwe
    print("request.args:\t", request.args, "\n")
    for i in request.args:
        print("arg:\t\t", i)
        print("get:\t\t", request.args.get(i))
        print("getlist:\t", request.args.getlist(i))
        print()
    g.arg0 = request.args.get('arg0')
    g.args = request.args
    return render_template("auth/example_page.html", page_info=LayoutPI(title="Page title"))


@auth_page_bp.route('/login', methods=['GET', 'POST'])
def login():
    err_list = []
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        err_list += form_validation_errors_for_login(email=email, password=password)
        web_user = db.get_webuser_with_email(email=email)
        if not err_list and web_user and hasher.verify(password, web_user.password_hash) and web_user.user_type in [
            WebUser.USER_TYPE.WORKPLACE_MANAGER, WebUser.USER_TYPE.ADMIN]:
            login_user(web_user)
            next_page = request.args.get("next", url_for("index"))
            return redirect(next_page)
        else:
            err_list.append("Email or password not correct and this page is for workplace managers")

    for err in err_list:
        flash(err, "danger")
    return render_template('login.html')


@auth_page_bp.route('/register', methods=["GET", "POST"])
def register():
    err_list = []
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        password = request.form['password']
        # TODO
        password_verification = request.form['password']
        email = request.form['email']

        web_user = db.get_webuser_with_email(email=email)
        if web_user:
            err_list.append("This email address already exist.")
        if password_verification != password:
            err_list.append("Passwords do not match.")
        err_list += form_validation_errors_for_register(name=name, surname=surname, email=email, password=password,
                                                        password_verification=password_verification)

        if not err_list:
            password_hash = hasher.hash(password)
            db.add_webuser(email=email, name=name, surname=surname,
                           password_hash=password_hash, user_type=WebUser.USER_TYPE.WORKPLACE_MANAGER)
            return redirect(url_for("auth_page_bp.login"))

    for err in err_list:
        flash(err, "danger")
    return render_template('register.html')
