from dbconfig import MONGO_URI, DB
from pymongo import MongoClient

"""
Base class for tables

Children of this class must overload 'get_table_name()' method
"""


class Db():

    def __enter__(self):
        self.client = MongoClient(MONGO_URI)
        db = self.client[DB]
        table = db[self.get_table_name()]
        return table

    def __exit__(self, type, value, traceback):
        self.client.close()

    def get_table_name(self):
        raise Exception("Table Name not overloaded. Please overload")