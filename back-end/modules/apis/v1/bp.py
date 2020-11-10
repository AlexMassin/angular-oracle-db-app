from flask import Blueprint
from flask_restplus import Api

bp = Blueprint('api', __name__)
api = Api(bp, version='1.0', prefix='crud', title='Double A DBMS API', description='A simple DBMS API linked to an Oracle DB.')
ns = api.namespace('crud', description='Version 1')