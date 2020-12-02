# @author Alex Gomes
# @create date 2020-11-09 22:09:18
# @modify date 2020-12-01 23:19:15
# @desc [The controller for the database, handling communication to the db through this component.]

from modules.apis.v1.db import engine as orcl_engine
from modules.apis.v1.db import stamp_queries
from modules.config import config

from celery import Celery
import sqlparse

worker = Celery(__name__, broker=config['CELERY_BROKER_URL'], backend=config['CELERY_RESULT_BACKEND'])

class DBTasks:
    @staticmethod
    @worker.task()
    def fib_task(n:int) -> int:
        if n <= 1:
            return n
        else:
            return(DBTasks.fib_task(n-1) + DBTasks.fib_task(n-2))

    @staticmethod
    @worker.task()
    def tail_recursive_fib_task(n:int, m:int=0, acc:int=1) -> int:
        if n == 0:
            return m
        if n == 1:
            return acc
        return DBTasks.tail_recursive_fib_task(n-1, acc, m + acc)

    @staticmethod
    @worker.task
    def ping_orcl_task():
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            errors = []
            raw = "SELECT 1 FROM DUAL;"
            try:
                proxy = connection.execute(raw.replace(";", ""))
                return {"query": raw, "responses": [dict(row) for row in proxy], "errors": errors}
            except Exception as e:
                return {"query": raw, "responses": "Task successful", "errors": errors}

    @staticmethod
    @worker.task
    def create_task():
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            errors = []
            for stmt in sqlparse.split(stamp_queries["CREATE"]):
                try:
                    proxy = connection.execute(stmt.replace(";", ""))
                except Exception as e:
                    if not str(e) in config["ERR_EXCPTS"]:
                        errors.append(str(e))
            return {"query": stamp_queries["CREATE"], "responses": "Task successful", "errors": errors}

    @staticmethod
    @worker.task
    def destroy_task():
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            errors = []
            for stmt in sqlparse.split(stamp_queries["DESTROY"]):
                try:
                    proxy = connection.execute(stmt.replace(";", ""))
                except Exception as e:
                    if not str(e) in config["ERR_EXCPTS"]:
                        errors.append(str(e))
            return {"query": stamp_queries["DESTROY"], "responses": "Task successful", "errors": errors}

    @staticmethod
    @worker.task
    def populate_task():
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            errors = []
            for stmt in sqlparse.split(stamp_queries["POPULATE"]):
                try:
                    proxy = connection.execute(stmt.replace(";", ""))
                except Exception as e:
                    if not str(e) in config["ERR_EXCPTS"]:
                        errors.append(str(e))
            return {"query": stamp_queries["POPULATE"], "responses": "Task successful", "errors": errors}

    @staticmethod
    @worker.task
    def get_table_task(tbl):
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            raw = f"SELECT * FROM {tbl};"
            try:
                proxy = connection.execute(raw.replace(";", ""))
                return {"query": raw, "responses": [dict(row) for row in proxy], "errors": []}
            except Exception as e:
                return {"query": raw, "responses": "Task successful", "errors": [str(e)]}

    @staticmethod
    @worker.task
    def query_tables_task(q):
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            raw = stamp_queries["QUERIES"][q]
            responses = []
            errors = []
            for stmt in sqlparse.split(raw):
                try:
                    proxy = connection.execute(stmt.replace(";", ""))
                    responses += [dict(row) for row in proxy]
                except Exception as e: 
                    if not str(e) in config["ERR_EXCPTS"]:
                        errors.append(str(e))
            return {"query": raw, "responses": responses, "errors": errors}

    @staticmethod
    @worker.task
    def raw_query_task(q):
        with orcl_engine.connect().execution_options(autocommit=True) as connection:
            responses = []
            errors = []
            for stmt in sqlparse.split(q):
                try:
                    proxy = connection.execute(stmt.replace(";", ""))
                    responses += [dict(row) for row in proxy]
                except Exception as e:
                    if not str(e) in config["ERR_EXCPTS"]:
                        errors.append(str(e))
            if not responses:
                return {"query": q, "responses": "Task successful", "errors": errors}
            return {"query": q, "responses": responses, "errors": errors}

class DBController:
    Tasks = DBTasks()

    def __init__(self):
        self.engine = orcl_engine
        self.stamp_queries = stamp_queries

    def ping(self):
        task = self.Tasks.ping_orcl_task.delay()
        return task.get()

    def create(self):
        task = self.Tasks.create_task.delay()
        return task.get()

    def destroy(self):
        task = self.Tasks.destroy_task.delay()
        return task.get()

    def populate(self):
        task = self.Tasks.populate_task.delay()
        return task.get()

    def get_table(self, tbl):
        task = self.Tasks.get_table_task.delay(tbl)
        return task.get()

    def query_tables(self, q):
        task = self.Tasks.query_tables_task.delay(q)
        return task.get()

    def raw_query(self, q):
        task = self.Tasks.raw_query_task.delay(q)
        return task.get()

    def test(self, n):
        print("Received test request")
        if (n < 0):
            "INVALID"
        if (n > 27):
            task = self.Tasks.tail_recursive_fib_task.delay(n)
        else:
            task = self.Tasks.fib_task.delay(n)
        return task.get()

worker.tasks.register(DBTasks.fib_task)
worker.tasks.register(DBTasks.tail_recursive_fib_task)
worker.tasks.register(DBTasks.ping_orcl_task)
worker.tasks.register(DBTasks.create_task)
worker.tasks.register(DBTasks.destroy_task)
worker.tasks.register(DBTasks.populate_task)
worker.tasks.register(DBTasks.get_table_task)
worker.tasks.register(DBTasks.query_tables_task)
worker.tasks.register(DBTasks.raw_query_task)

### IMPORTANT ON WHY SEMICOLON AND MULTIPLE STATEMENTS RESULT IN AN ERROR:
# https://stackoverflow.com/questions/20607524/newline-charter-n-gives-java-sql-sqlexception-ora-00911-invalid-character-n
# Easy solution: split sql expressions into individual units, execute each unit, and merge results from each unit
