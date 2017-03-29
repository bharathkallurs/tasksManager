import os
from pymongo import MongoClient

#Database setting
MONGO_URI = os.environ.get('MONGOHQ_URL') if os.environ.get('MONGOHQ_URL') is not None \
    else 'mongodb://localhost:27017/heroku_tr2f0kzz'

client = MongoClient(MONGO_URI)
DB = client.get_default_database().name if client.get_default_database() is not None else 'task_database'
client.close()
