from flask import Flask, redirect
from flask_restplus import Api

from modules.apis.v1.bp import bp as bp_v1
from modules.config import config

app = Flask(__name__)

app.register_blueprint(bp_v1, url_prefix='/api/v1')

#crud = api.Model('CRUD', {
#    
#})

@app.route('/')
def redir():
    return redirect(config['LATEST_API_VERSION'])

from modules.apis.v1 import endpoints