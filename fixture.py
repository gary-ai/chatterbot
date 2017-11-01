#!/usr/bin/env python
import json
import os
from pymongo import MongoClient

# use ignored .dist config file only if config.json doesn't exist
if not os.path.isfile("./fixtures/config.json"):
    os.system("cp ./fixtures/config.json.dist ./fixtures/config.json")
config_json = open("./fixtures/config.json", 'r')
config_json = json.loads(config_json.read())
users_json = open("./fixtures/users.json", 'r')
users_json = json.loads(users_json.read())
intents_json = open("./fixtures/intents.json", 'r')
intents_json = json.loads(intents_json.read())

connection = MongoClient("mongodb://mongo:27017")
db = connection.gary_db
users_collection = db.users
config_collection = db.config
intents_collection = db.intents
db.users.drop()
db.config.drop()
db.intents.drop()

for item in users_json['users']:
    users_collection.insert(item)
for item in config_json['config']:
    config_collection.insert(item)
for item in intents_json['intents']:
    intents_collection.insert(item)
