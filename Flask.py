'''
from flask import Flask, redirect, url_for, request,render_template


app = Flask(__name__)


@app.route('/')
def success():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
'''

import flask
import dash
import dash_html_components as html
from flask import render_template


server = flask.Flask(__name__)

@server.route('/')
def index():
    return render_template('index.html')

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

app.layout = html.Div("My Dash app")

if __name__ == '__main__':
    app.run_server(debug=True)