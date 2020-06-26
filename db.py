from pymongo import MongoClient 

def get_connection():
    return MongoClient()