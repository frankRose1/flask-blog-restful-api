"""
  Default application settings, used in development
"""
import os

DEBUG = True
SECRET_KEY = os.environ['SECRET_KEY']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
UPLOADED_IMAGES_DEST = os.path.join('static', 'images')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True