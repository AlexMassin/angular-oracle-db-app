# @author Alex Gomes
# @create date 2020-11-09 20:01:47
# @modify date 2020-11-18 21:40:02
# @desc [API factory.]

from flask import Flask, redirect
from flask_restplus import Api, Resource

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