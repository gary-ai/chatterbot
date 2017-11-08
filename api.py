import requests

from flask import Flask, jsonify, url_for, redirect, request
from flask_pymongo import PyMongo
from flask_restful import Api, Resource
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
    def get(user_id=None, channel=None, command=None):
        if user_id and channel and command:
            rep = chat_response(command, user_id)
            print rep
            if rep and 'exec' in rep:
                cmd = mongo.db.config.find_one({"name": rep.split(' ', 1)[1]})
                if cmd and cmd['name'] and cmd['type'] == "api":
                    try:
                        r = requests.get(cmd['url']).json()
                        if r and cmd and 'success' in cmd:
                            return {"response": {"message": cmd['success']}}
                        else:
                            return {"response": {"message": r['response']}}
                    except ValueError:
                        print "nlp: can't decode json from home api, might be down"
                    return {"response": {"message": "Hum, connection error with your home installation"}}
                else:
                    return {"response": {"message": "Error between intent conf and config collection."}}
            elif rep:
                return {"response": {"message": rep}}
            else:
                return {"response": {"message": "Please repeat, I don't understand ?  :robot_face:"}}
        else:
            return {"response": {"message": "I need user_id, channel and messages to response"}}


api = Api(app)
api.add_resource(GaryBotResponse, "/api/message/<string:user_id>/<string:channel>/<string:command>/", endpoint="message")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
