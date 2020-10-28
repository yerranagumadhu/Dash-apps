from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from flask_app import flask_app
from app1 import app as app1
from app2 import app as app2


app1.enable_dev_tools(debug=True)
app2.enable_dev_tools(debug=True)

#http://localhost:8050/

application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    '/app2': app2.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)