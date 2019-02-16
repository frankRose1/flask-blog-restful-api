from flask import url_for, Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity, jwt_required

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
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return {'current_user': user_schema.dump(user)}, 200

    @classmethod
    @fresh_jwt_required
    def put(cls):
        # updated_user_data = user_schema.load(request.get_json(), partial=('password'))
        return {'message': 'put request to users api'}

    @classmethod
    @fresh_jwt_required
    def delete(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        # TODO delete all of the associated posts/comments
        user.delete_from_db()
        return (
            '',
            204,
            {'Location': 'resources.users.users'}
        )



users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    User,
    '/users',
    endpoint='users'
)
