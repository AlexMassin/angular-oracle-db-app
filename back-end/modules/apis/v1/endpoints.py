import os

from flask import send_from_directory
from flask_restplus import Resource, Api

from modules import app
from modules.apis.v1.bp import ns
from modules.apis.v1.db_controller import DBController, stamp_queries

@ns.route('/test')
class Test(Resource):
    '''Testing API'''
    @ns.doc('test api')
    def get(self):
        '''basic msg carrying request'''
        return {'CREATE': stamp_queries}