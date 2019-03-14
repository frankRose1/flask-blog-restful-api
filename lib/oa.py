"""This file contains the info regarding the github client"""
import os
from flask_oauthlib.client import OAuth

oauth = OAuth()

github = oauth.remote_app(
    'github',
    consumer_key=os.environ.get('GITHUB_CONSUMER_KEY'),
    consumer_secret=os.environ.get('GITHUB_CONSUMER_SECRET'),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    # if using oauth 1.0 this would need to be a URL
    request_token_url=None,
    # once the user has authorized our app, a post request is sent to github for their accees token
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth'
)