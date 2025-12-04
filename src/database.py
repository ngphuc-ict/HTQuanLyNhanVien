import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

def get_database():
    try:
        client = MongoClient(mongo_uri)
        return client[db_name]
    except Exception as e:
        print("Kết nối không thành công!")
        print(e)