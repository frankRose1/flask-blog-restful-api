import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from ma import ma
from resources.posts import posts_api
from resources.users import users_api
from resources.auth import auth_api
from resources.comments import comments_api

API_PREFIX = '/api/v1'

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)


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
    return 'Hello'


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
    app.run(debug=True, host='0.0.0.0', port=5000)
