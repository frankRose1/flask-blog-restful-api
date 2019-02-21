from flask import url_for, Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import fresh_jwt_required, get_jwt_identity, jwt_required

from models.user import UserModel
from lib.schemas import UserSchema
from lib.mailer import MailException
USER_NOT_FOUND = 'User not found.'
USERNAME_TAKEN = 'That username has already been taken.'
EMAIL_TAKEN = 'That email has already been taken.'

user_schema = UserSchema()


class User(Resource):

    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {'message': USERNAME_TAKEN}, 400

        if UserModel.find_by_email(user.email):
            return {'message': EMAIL_TAKEN}, 400

        user.password = UserModel.set_password(user.password)
        try:
            user.save_to_db()
            user.send_confirmation_email()
        except MailException as e:
            user.delete_from_db()
            return {'message': str(e)}, 500

        return (
            '',
            201,
            {'Location': url_for('resources.auth.login')}
        )

    @classmethod
    @jwt_required
    def get(cls):
        """Returns the currently signed in user"""
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return {'current_user': user_schema.dump(user)}, 200

    @classmethod
    @fresh_jwt_required
    def put(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        
        updated_user_data = user_schema.load(request.get_json(), partial=('password',))
        # see if username is being changed
        new_username = updated_user_data.username
        if new_username != user.username:
            existing_user = UserModel.find_by_username(new_username)
            if existing_user:
                return {'message': USERNAME_TAKEN}, 400
            else:
                user.username = new_username

        user.name = updated_user_data.name
        user.save_to_db()
        return (
            '',
            204,
            {'Location': url_for('resources.users.users')}
        )

    @classmethod
    @fresh_jwt_required
    def delete(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.delete_from_db()
        return (
            '',
            204,
            {'Location': 'resources.users.users'}
        )


class UserProfile(Resource):

    @classmethod
    def get(cls, username):
        user = UserModel.find_by_username(username)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        return {'user': user_schema.dump(user)}, 200


class ActivateUserAccount(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        
        user.activated = True
        user.save_to_db()
        return (
            {'message': 'Your account has been activated.'},
            200,
            {'Location': url_for('resources.auth.login')}
        )


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    User,
    '/users',
    endpoint='users'
)
api.add_resource(
    UserProfile,
    '/users/<username>',
    endpoint="user_profile"
)
api.add_resource(
    ActivateUserAccount,
    '/user/activate_account/<int:user_id>',
    endpoint='activate_account'
)
