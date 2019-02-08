from flask import Blueprint, request
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token
from argon2.exceptions import VerifyMismatchError


from schemas.user import UserSchema
from models.user import UserModel

user_schema = UserSchema()

INVALID_CREDENTIALS = 'Incorrect email or password.'


class Login(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=('name',))
        user = UserModel.find_by_username(user_data.username)
        if not user:
            return {'message': INVALID_CREDENTIALS}, 400
        try:
            user.verify_password(user_data.password)
        except VerifyMismatchError:
            return {'message': INVALID_CREDENTIALS}, 400
        
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}


auth_api = Blueprint('resources.auth', __name__)
api = Api(auth_api)
api.add_resource(
    Login,
    '/auth/login',
    endpoint='login'
)
