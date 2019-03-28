from flask import Blueprint, request, g, url_for
from flask_restful import Resource, Api
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity)
from argon2.exceptions import VerifyMismatchError

from lib.oa import github
from lib.schemas import UserSchema
from models.user import UserModel

user_schema = UserSchema()

INVALID_CREDENTIALS = 'Incorrect email or password.'
NOT_ACTIVATED = 'This account has not been activated yet. Please check the email account that you signed up with.'


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

        if not user.activated:
            return {'message': NOT_ACTIVATED}, 400

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200


class RefreshToken(Resource):

    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class GithubLogin(Resource):
    """This resource will confirm if a user allows github to release their credentials"""
    @classmethod
    def get(cls):
        return github.authorize(callback=url_for('resources.auth.github_authorized', external=True))



class GithubAuthorization(Resource):
    """This resource is for when a user lets github give us their credentials. Github will forward the info to us
        so that we can make a post request to github to retrieve the user's access token.
    """
    @classmethod
    def get(cls):
        res = github.authorized_response()
        if res is None or res['access_token'] is None:
            # errors from github would look like ..?error=Something%20went%20wrong&error_description=Something%20else
            error_response = {
                'error': request.args['error'],
                'error_description': request.args['error_description']
            }
            return error_response, 400
        
        g.access_token = res['access_token']
        # gets the user info from the github client
        github_user = github.get('user')
        github_username = github_user.data['login']
        return {'user': github_user.data}
        # user = UserModel.find_by_username(github_username)
        # if not user:
        #     user = UserModel.find_by_username(username=github_username, password=None,)
        #     user.save_to_db()
        
        # access_token = create_access_token(identity=user.id, fresh=True)
        # refresh_token = create_refresh_token(user.id)
        # return {'access_token': access_token, 'refresh_token': refresh_token}, 200


auth_api = Blueprint('resources.auth', __name__)
api = Api(auth_api)
api.add_resource(
    Login,
    '/auth/login',
    endpoint='login'
)
api.add_resource(
    GithubLogin,
    '/auth/github',
    endpoint='github_login'
)
api.add_resource(
    GithubAuthorization,
    '/auth/github/authorized',
    endpoint='github_authorized'
)
api.add_resource(
    RefreshToken,
    '/auth/refresh',
    endpoint='refresh'
)
