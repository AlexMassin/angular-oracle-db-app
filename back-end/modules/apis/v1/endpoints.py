# @author Alex Gomes
# @create date 2020-11-09 20:05:39
# @modify date 2020-11-18 22:03:01
# @desc [API endpoints for the front end to communicate with the backend and db.]

import os

from flask_restplus import Resource, Api

from modules import app
from modules.apis.v1.bp import ns_crud, ns_stats, dbc

#########################
#                       #
#    Stats Endpoints    #
#                       #
#########################
@ns_stats.route('/ping')
class Ping(Resource):
    '''Testing API'''
    @ns_stats.doc('ping api')
    def get(self):
        '''basic msg carrying response'''
        return {'ping': 'pong!'}

#########################
#                       #
#     CRUD Endpoints    #
#                       #
#########################

@ns_crud.route('/create')
class Ping(Resource):
    '''Testing API'''
    @ns_crud.doc('ping api')
    def get(self):
        '''basic msg carrying response'''
        return {'CREATE': stamp_queries['CREATE']}