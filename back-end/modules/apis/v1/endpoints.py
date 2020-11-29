# @author Alex Gomes
# @create date 2020-11-09 20:05:39
# @modify date 2020-11-28 19:43:58
# @desc [API endpoints for the front end to communicate with the backend and db.]

import os

from flask_restplus import Resource, Api

from modules import app
from modules.apis.v1.bp import ns_crud, ns_stats, dbc
from modules.apis.v1.db import stamp_queries

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
        err = dbc.create()
        return {'CREATE': stamp_queries['CREATE'], 'ERR:': err}

@ns_crud.route('/destroy')
class Destroy(Resource):
    @ns_crud.doc('drop tables')
    def get(self):
        '''Drop all tables'''
        err = dbc.destroy()
        return {'DESTROY': stamp_queries['DESTROY'], 'ERR:': err}

@ns_crud.route('/populate')
class Populate(Resource):
    @ns_crud.doc('populate tables')
    def get(self):
        '''Populate all tables with migration data'''
        err = dbc.populate()
        return {'POPULATE': stamp_queries['POPULATE'], 'ERR:': err}

@ns_crud.route('/get-table/<string:tbl>')
class GetTable(Resource):
    @ns_crud.doc('Return all values from a table.')
    def get(self, tbl):
        '''SELECT * FROM tbl'''
        r = dbc.get_table(tbl)
        return {'result': r}

@ns_crud.route('/sample-query/<int:q>')
class QueryTable(Resource):
    @ns_crud.doc('Return the results from a list of queries at index.')
    def get(self, q):
        '''Return results of sample queries.'''
        r = dbc.query_tables(q)
        return {'result': r}
