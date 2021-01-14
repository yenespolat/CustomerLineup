import os

from flask import Flask, render_template
from pony.flask import Pony

from customer_lineup.auth.api import auth_api_bp
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

app = Flask(
    __name__, instance_relative_config=True,
    template_folder='utils/templates', static_folder='utils/static', static_url_path='/assets'
)
app.secret_key = os.getenv("SECRET_KEY")
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
