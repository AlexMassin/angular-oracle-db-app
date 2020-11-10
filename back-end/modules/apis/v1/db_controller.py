from modules.apis.v1.db import engine as orcl_engine
from modules.apis.v1.db import stamp_queries

class DBController:
    def __init__(self):
        engine = orcl_engine

    def create(self):
        with engine.connect() as connection:
            R = connection.execute(stamp_queries['CREATE'])