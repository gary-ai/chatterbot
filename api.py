
from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
from bson.objectid import ObjectId
from chatbot import chat_response

app = Flask(__name__)
app.config['MONGO_HOST'] = 'mongo'
app.config['MONGO_PORT'] = 27017
app.config["MONGO_DBNAME"] = "gary_db"
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
mongo = PyMongo(app, config_prefix='MONGO')


class GaryBotResponse(Resource):
    @staticmethod
    def get(id=None, command=None, channel=None):
        if id and command and channel:
            print id, command, channel
            user = mongo.db.users.find_one({"user_id": id})
            print user
            rep = chat_response(command, id)
            print rep
            if rep and 'exec' in rep:
                cmd = mongo.db.config.find_one({"_id": ObjectId(rep.split(' ', 1)[1])})
                if cmd and cmd['name']:
                    print cmd['name']
                    return {"response": {"message": cmd['success']}}
            elif rep:
                return {"response": {"message": rep}}
            else:
                return {"response": {"message": "hum, I'm stuck. sorry. bye."}}


class Index(Resource):
    def get(self):
        return redirect(url_for("message"))


api = Api(app)
api.add_resource(Index, "/", endpoint="index")
api.add_resource(GaryBotResponse, "/api/message/<string:id>/<string:channel>/<string:command>/", endpoint="message")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
