# @author Alex Gomes
# @create date 2020-11-09 22:09:18
# @modify date 2020-11-18 22:02:39
# @desc [The controller for the database, handling communication to the db through this component.]

from modules.apis.v1.db import engine as orcl_engine
from modules.apis.v1.db import stamp_queries

class DBController:
    def __init__(self):
        self.engine = orcl_engine
        self.stamp_queries = stamp_queries

    def create(self):
        with self.engine.connect() as connection:
            R = connection.execute(stamp_queries['CREATE'])
            print(R)