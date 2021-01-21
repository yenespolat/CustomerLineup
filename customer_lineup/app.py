import os

from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_login import LoginManager, current_user
from pony.flask import Pony

from customer_lineup.auth.api import auth_api_bp
from customer_lineup.auth.authorization import admin_required
from customer_lineup.auth.db import get_webuser_with_id
from customer_lineup.auth.page import auth_page_bp
from customer_lineup.blueprint_template.api import blueprint_template_api_bp
from customer_lineup.blueprint_template.page import blueprint_template_page_bp
from customer_lineup.comment.api import comment_api_bp
from customer_lineup.comment.page import comment_page_bp
from customer_lineup.queue_.api import queue_api_bp
from customer_lineup.queue_.page import queue_page_bp
from customer_lineup.utils import CustomJSONEncoder
from customer_lineup.workplace.api import workplace_api_bp
from customer_lineup.workplace.page import workplace_page_bp

from customer_lineup.admin.admin import admin_page_bp

app = Flask(
    __name__, instance_relative_config=True,
    template_folder='utils/templates', static_folder='utils/static', static_url_path='/assets'
)
app.secret_key = 'secretkey'
#app.secret_key = os.getenv("SECRET_KEY")
app.json_encoder = CustomJSONEncoder

Pony(app)

app.register_blueprint(blueprint_template_api_bp, url_prefix="/api/blueprint_template")
app.register_blueprint(blueprint_template_page_bp, url_prefix="/blueprint_template")
app.register_blueprint(auth_api_bp, url_prefix="/api/auth")
app.register_blueprint(auth_page_bp, url_prefix="/auth")
app.register_blueprint(comment_api_bp, url_prefix="/api/comment")
app.register_blueprint(comment_page_bp, url_prefix="/comment")
app.register_blueprint(queue_api_bp, url_prefix="/api/queue")
app.register_blueprint(queue_page_bp, url_prefix="/queue")
app.register_blueprint(workplace_api_bp, url_prefix="/api/workplace")
app.register_blueprint(workplace_page_bp, url_prefix="/workplace")

app.register_blueprint(admin_page_bp, url_prefix="/admin")

lm = LoginManager()

@lm.user_loader
def load_user(wu_id):
    return get_webuser_with_id(id=wu_id)


lm.init_app(app)
lm.login_message_category = 'danger'
lm.login_message = u"Please login for access this page."
lm.login_view = "auth_page_bp.login"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/application')
def download():
    uploads_dir = os.path.join('.\\apk')
    return send_from_directory(uploads_dir, 'CustomerLineUp.apk')

@app.route('/loaderio-eea58de1064be82a154acd4ba76aece9/')
def loaderio():
    return 'loaderio-eea58de1064be82a154acd4ba76aece9'

@app.route('/load-test-api')
def load_test():
    args = request.args
    text = args.get('text')
    return jsonify(result=True, msg=text)



if __name__ == '__main__':
    app.run(debug=True)
