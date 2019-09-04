from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
api = Api(app)
app.config.from_object(os.getenv('APP_SETTINGS'))

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


api.add_resource(UsersPing, '/users/ping')
