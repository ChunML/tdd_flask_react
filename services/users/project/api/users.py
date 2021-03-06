from flask import Blueprint, request, render_template
from flask_restful import Resource, Api
from project import db
from project.api.models import User
from project.api.utils import authenticate_restful, is_admin
from sqlalchemy import exc


users_blueprint = Blueprint('users', __name__, template_folder='./templates')
api = Api(users_blueprint)


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(
            username=username, email=email, password=password))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)


class UsersPing(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }


class UsersList(Resource):
    method_decorators = {'post': [authenticate_restful]}

    def get(self):
        users = User.query.all()
        response_object = {
            'data': [user.to_json() for user in users],
            'status': 'success'
        }
        return response_object, 200

    def post(self, resp):
        post_data = request.get_json()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        if not is_admin(resp):
            response_object['message'] = \
                'You do not have the permission to do that.'
            return response_object, 401
        if not post_data:
            return response_object, 400
        username = post_data.get('username')
        email = post_data.get('email')
        password = post_data.get('password')
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(
                    username=username, email=email, password=password))
                db.session.commit()
                response_object['status'] = 'success'
                response_object['message'] = f'{email} was added!'
                return response_object, 201
            else:
                response_object['message'] = 'Sorry. ' \
                    'That email already exists.'
                return response_object, 400
        except (exc.IntegrityError, ValueError):
            db.session.rollback()
            return response_object, 400


class Users(Resource):
    def get(self, user_id):
        response_object = {
            'message': 'User does not exist.',
            'status': 'fail'
        }
        try:
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return response_object, 404

            response_object = {
                'data': {
                    'id': user_id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                },
                'status': 'success'
            }
            return response_object, 200
        except ValueError:
            return response_object, 404


api.add_resource(UsersPing, '/users/ping')
api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<user_id>')
