# database.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["website_paper"]

def get_collection(collection_name):
    return db[collection_name]
