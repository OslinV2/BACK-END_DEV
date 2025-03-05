from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import variables
import os

class MongoConnect(object):
    
    def __init__(self, is_log: bool = False):
        self.is_log = is_log
        self.client = None
        self.db = None

    def open_connections(self, uri=None):
        if self.client is None or not self.is_connected():
            if self.is_log:
                self.db_name = "logging"
            else:
                self.db_name = variables.DATABASE
            
            if uri is None:
                uri = variables.MONGODBPROD_URI
            if uri is None:
                raise ValueError("URI do MongoDB não fornecido.")
            
            self.client = MongoClient(uri)
            self.db = self.client[self.db_name]

    def close_connections(self):
        self.client.close()

    def is_connected(self) -> bool:
        """
        Verifica se a conexão com o banco de dados está ativa.

        Returns:
            bool: True se a conexão estiver ativa, False caso contrário.
        """
        if self.client is None:
            return False
        try:
            self.client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False

    def get_collection(self, collection):
        self.collection = self.db[collection]
        return self.collection

    def get_one(self, query):
        return self.collection.find_one(query)

    def get_list_collection_name(self):
        return self.db.list_collection_names()

    def insert_one(self, collection, query):
        container = self.db[collection]
        return container.insert_one(query)
