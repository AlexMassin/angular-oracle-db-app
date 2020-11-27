# @author Alex Gomes
# @create date 2020-11-09 22:09:18
# @modify date 2020-11-27 15:02:41
# @desc [The controller for the database, handling communication to the db through this component.]

from modules.apis.v1.db import engine as orcl_engine
from modules.apis.v1.db import con as orcl_con
from modules.apis.v1.db import stamp_queries
from modules.config import config

from celery import Celery
import sqlparse

worker = Celery(__name__, broker=config['CELERY_BROKER_URL'], backend=config['CELERY_RESULT_BACKEND'])

class DBController:
    @staticmethod
    @worker.task(name='dbc.test')
    def fib_task(n:int) -> int:
        if n <= 1:
            return n
        else:
            return(DBController.fib_task(n-1) + DBController.fib_task(n-2))

    @staticmethod
    @worker.task(name='dbc.test_deferral')
    def tail_recursive_fib_task(n:int, m:int=0, acc:int=1) -> int:
        if n == 0:
            return m
        if n == 1:
            return acc
        return DBController.tail_recursive_fib_task(n-1, acc, m + acc)

    @staticmethod
    @worker.task
    def create_task():
        with orcl_con.execution_options(autocommit=True) as connection:
            R = connection.execute(stamp_queries['CREATE'])

    @staticmethod
    @worker.task
    def destroy_task():
        with orcl_con.execution_options(autocommit=True) as connection:
            R = connection.execute(stamp_queries['DESTROY'])

    @staticmethod
    @worker.task
    def reset_task():
        with orcl_con.execution_options(autocommit=True) as connection:
            R = connection.execute(stamp_queries['RESET'])

    @staticmethod
    @worker.task
    def see_accounts_task():
        with orcl_con.execution_options(autocommit=True) as connection:
            raw = r"SELECT * FROM Accounts; SELECT * FROM Customers;"
            stmts = sqlparse.split(raw)
            results = []
            for stmt in stmts:
                proxy = connection.execute(stmt.replace(";", ""))
                results += [dict(row) for row in proxy]
            return results

    def __init__(self):
        self.engine = orcl_engine
        self.stamp_queries = stamp_queries

    def create(self):
        DBController.create_task.delay()

    def destroy(self):
        DBController.destroy_task.delay()

    def reset(self):
        print(f"Sending query:\n{stamp_queries['RESET']}")
        DBController.reset_task.delay()

    def see_accounts(self):
        print(f"Sending query:\nSELECT * FROM Accounts")
        task = DBController.see_accounts_task.delay()
        return task.get()

    def test(self, n):
        print("Received test request")
        if (n < 0):
            "INVALID"
        if (n > 27):
            task = DBController.tail_recursive_fib_task.delay(n)
        else:
            task = DBController.fib_task.delay(n)
        return task.get()

worker.tasks.register(DBController.fib_task)
worker.tasks.register(DBController.tail_recursive_fib_task)
worker.tasks.register(DBController.create_task)
worker.tasks.register(DBController.destroy_task)
worker.tasks.register(DBController.see_accounts_task)

### IMPORTANT ON WHY SEMICOLON AND MULTIPLE STATEMENTS RESULT IN AN ERROR:
# https://stackoverflow.com/questions/20607524/newline-charter-n-gives-java-sql-sqlexception-ora-00911-invalid-character-n
# Easy solution: split sql expressions into individual units, execute each unit, and merge results from each unit
