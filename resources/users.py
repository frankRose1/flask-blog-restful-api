from flask import url_for, Blueprint, request
from flask_restful import Resource, Api
from marshmallow import ValidationError

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class User(Resource):

    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_username(user.username):
            return {'message': 'That username has already been taken.'}, 400

        user.save_to_db()
        return (
            '',
            201,
            {'Location': '/api/v1/auth'}
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
