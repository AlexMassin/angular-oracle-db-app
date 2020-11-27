# @author Alex Gomes
# @create date 2020-11-09 20:05:39
# @modify date 2020-11-27 15:45:56
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

@ns_stats.route('/test-fib-<int:n>')
class Test(Resource):
    @ns_stats.doc('test redis')
    def get(self, n):
        '''Test MQ + BGW'''
        r = dbc.test(n)
        if (n > 27):
            return {f'fib({n})': r, 'msg': 'To prevent overflow of long tasks, deferred fibonacci calls to a tail recursive implementation for n > 27.'}
        return {f'fib({n})': r}

#########################
#                       #
#     CRUD Endpoints    #
#                       #
#########################

@ns_crud.route('/create')
class Create(Resource):
    @ns_crud.doc('create tables')
    def get(self):
        '''Create all tables'''
        dbc.create()
        return {'CREATE': 'scheduled task successfully.'}

@ns_crud.route('/destroy')
class Destroy(Resource):
    @ns_crud.doc('drop tables')
    def get(self):
        '''Drop all tables'''
        dbc.destroy()
        return {'DESTROY': 'scheduled task successfully.'}

@ns_crud.route('/reset')
class Reset(Resource):
    @ns_crud.doc('reset tables')
    def get(self):
        '''Reset all tables'''
        dbc.reset()
        return {'RESET': 'scheduled task successfully.'}

@ns_crud.route('/see_accounts')
class Reset(Resource):
    @ns_crud.doc('view accounts tables')
    def get(self):
        '''SELECT * FROM Accounts'''
        r = dbc.see_accounts() # currently returns accounts and customers
        return {'msg': 'scheduled task successfully.', 'result': f"{r}"}
