from pymongo import MongoClient


class DatabaseCalls():
    def __init__(self, document):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.collection = self.client["Project_ezana"]
        self.document = self.collection[document]

    def find_one(self, query):
        filter_query = {"input": query}

        # Perform the find operation with the filter
        result = self.document.find(filter_query)

        # Iterate over the result set and print each document
        for document in result:
            return document['response']

    def insert_one(self, object):
        self.document.insert_one(object)
