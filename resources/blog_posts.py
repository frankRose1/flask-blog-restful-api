import datetime
from flask import Blueprint
from flask_restful import Resource, Api
from models.blogpost import BlogPost


class BlogPostList(Resource):

    def post(self):
        return {'title': 'Random Title', '': datetime.datetime.now()}, 201

    def get(self):
        return {'blog_posts': [
            {'title': 'Random Title', '': datetime.datetime.now()},
            {'title': 'another Title', '': datetime.datetime.now()}
        ]}


class Post(Resource):
    def get(self, post_id):
        return {'title': 'Random Title', '': datetime.datetime.now()}

    def put(self, post_id):
        return {'title': 'Random Title', '': datetime.datetime.now()}, 204

    def delete(self, post_id):
        return {'title': 'Random Title', '': datetime.datetime.now()}, 204


blog_posts_api = Blueprint('resources.blog_posts', __name__)
api = Api(blog_posts_api)
api.add_resource(
    BlogPostList,
    '/posts',
    endpoint='posts'
)
api.add_resource(
    Post,
    '/posts/<int:post_id>',
    endpoint='post'
)