# @author Alex Gomes
# @create date 2020-11-09 21:47:18
# @modify date 2020-11-27 15:26:28
# @desc [Blueprint for the API, including the API and namespaces.]

from flask import Blueprint
from flask_restplus import Api

from modules.apis.v1.db_controller import DBController

bp = Blueprint('api', __name__)
api = Api(bp, version='1.0', prefix='', title='Double A DBMS API', description='A simple DBMS API linked to an Oracle DB.')
ns_crud = api.namespace('crud', description='CREATE | READ | UPDATE | DELETE')
ns_stats = api.namespace('stats', description='STATISTICS')
dbc = DBController()