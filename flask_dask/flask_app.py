from flask import Flask
from flask import render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    return render_template('index.html')