__author__ = 'Akshay_Rahar'

import pymongo

class Database(object):

    URI="mongodb://akshay_rahar:mlabdb2016@ds013926.mlab.com:13926/upcomingmovies"

    DATABASE = None

    @staticmethod
    def initialize():
        client= pymongo.MongoClient(Database.URI, connect=False)
        Database.DATABASE= client['upcomingmovies']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_coloumn(collection,projection):
        return  Database.DATABASE[collection].find({}, {projection:1, "_id":0})

    @staticmethod
    def remove_all(collection):
        Database.DATABASE[collection].remove({})

