# @author Alex Gomes
# @create date 2020-11-09 20:05:39
# @modify date 2020-12-01 23:18:38
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
    @ns_stats.doc('ping api')
    def get(self):
        '''Test API connection'''
        return {'ping': 'pong!'}

@ns_stats.route('/test-fib-<int:n>')
class Test(Resource):
    @ns_stats.doc('test redis')
    def get(self, n):
        '''Test workers and message queue'''
        r = dbc.test(n)
        if (n > 27):
            return {f'fib({n})': r, 'msg': 'To prevent overflow of long tasks, deferred fibonacci calls to a tail recursive implementation for n > 27.'}
        return {f'fib({n})': r}

@ns_stats.route('/samples')
class SampleQueries(Resource):
    @ns_stats.doc('Return sample queries and their indices')
    def get(self):
        '''Sample queries'''
        result = []
        for i, q in enumerate(stamp_queries["QUERIES"]):
            result.append({"value": f'{i}', "viewValue": f'{q}'})
        return {"responses": result}

#########################
#                       #
#     CRUD Endpoints    #
#                       #
#########################

@ns_crud.route('/ping')
class Create(Resource):
    @ns_crud.doc('ping oracle')
    def get(self):
        '''Test DB connection'''
        result = dbc.ping()
        return result

@ns_crud.route('/create')
class Create(Resource):
    @ns_crud.doc('create tables')
    def get(self):
        '''Create all tables'''
        result = dbc.create()
        return result

@ns_crud.route('/destroy')
class Destroy(Resource):
    @ns_crud.doc('drop tables')
    def get(self):
        '''Drop all tables'''
        result = dbc.destroy()
        return result

@ns_crud.route('/populate')
class Populate(Resource):
    @ns_crud.doc('populate tables')
    def get(self):
        '''Populate all tables with migration data'''
        result = dbc.populate()
        return result

@ns_crud.route('/get-table/<string:tbl>')
class GetTable(Resource):
    @ns_crud.doc('Return all values from a table.')
    def get(self, tbl):
        '''SELECT * FROM tbl'''
        result = dbc.get_table(tbl)
        return result

@ns_crud.route('/sample-query/<int:q>')
class QueryTable(Resource):
    @ns_crud.doc('Return the results from a list of queries at index.')
    def get(self, q):
        '''Return results of sample queries.'''
        q_max = len(stamp_queries["QUERIES"]) - 1
        if (q > q_max):
            return {"query": "", "responses": "Task not scheduled.", "errors": [f"Invalid query index, range(0, {q_max})."]}
        result = dbc.query_tables(q)
        return result

@ns_crud.route('/raw-query/<string:q>')
class RawQuery(Resource):
    @ns_crud.doc('Execute raw query')
    def get(self, q):
        '''Send query to DB'''
        result = dbc.raw_query(q)
        return result