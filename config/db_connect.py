# database.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:50000/")
db = client["chat_history"]

def get_collection(collection_name):
    return db[collection_name]
