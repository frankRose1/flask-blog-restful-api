from flask import url_for, Blueprint, request
from flask_restful import Resource, Api

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class User(Resource):

    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {'message': 'That username has already been taken.'}, 400

        user.password = UserModel.set_password(user.password)
        user.save_to_db()
        return (
            '',
            201,
            {'Location': url_for('resources.auth.login')}
        )

    @classmethod
    def put(cls):
        return {'user': 'put request'}

    @classmethod
    def delete(cls):
        return {'user': 'delete request'}


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    User,
    '/users',
    endpoint='users'
)
