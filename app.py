import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_ipaddr
from marshmallow import ValidationError
from dotenv import load_dotenv

from lib.db import db
from lib.ma import ma
from lib.oa import oauth
from resources.posts import posts_api
from resources.users import users_api
from resources.auth import auth_api
from resources.comments import comments_api

API_PREFIX = '/api/v1'
daily_rate = os.environ.get('GLOBAL_DAILY_RATE')
hourly_rate = os.environ.get('GLOBAL_HOURLY_RATE')

app = Flask(__name__)
load_dotenv('.env', verbose=True)
app.config.from_object('default_config')
# any default config settings that need to be over-written can be changed the 
# file referred to by APPLICATION_SETTINS in .env
app.config.from_envvar('APPLICATION_SETTINGS')

jwt = JWTManager(app)

limiter = Limiter(
    app,
    default_limits=[daily_rate, hourly_rate],
    key_func=get_ipaddr
)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify(
        {
            'message': 'Authorization headers are missing or no access token was provided.',
            'error': 'Unauthorized'
         }
    ), 401


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify(
        {
            'message': 'The provided access token has expired.',
            'error': 'Expired token'
         }
    ), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify(
        {
            'message': 'Token is invalid.',
            'error': error
        }
    ), 422


@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to the blog API.'
    })


app.register_blueprint(posts_api, url_prefix=API_PREFIX)
app.register_blueprint(users_api, url_prefix=API_PREFIX)
app.register_blueprint(auth_api, url_prefix=API_PREFIX)
app.register_blueprint(comments_api, url_prefix=API_PREFIX)


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


if __name__ == '__main__':
    db.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
