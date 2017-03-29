import os
from pymongo import MongoClient

#Database setting

MONGO_URI = os.environ.get('MONGOHQ_URL') if os.environ.get('MONGOHQ_URL') is not None \
    else 'mongodb://heroku_tr2f0kzz:6vgb9kukuk3tg1berdjegh3vn4@ds033175.mlab.com:33175/heroku_tr2f0kzz'

client = MongoClient(MONGO_URI)
DB = client.get_default_database().name if client.get_default_database() is not None else 'task_database'
client.close()
