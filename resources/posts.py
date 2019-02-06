import datetime
from flask import Blueprint, request
from flask_restful import Resource, Api, url_for

from models.post import PostModel
from schemas.post import PostSchema
from marshmallow import ValidationError

post_schema = PostSchema()


class PostList(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        try:
            post = post_schema.load(data)
        except ValidationError as err:
            return err.messages, 400

        post.save_to_db()

        return (
            '',
            201,
            {'Location': url_for('resources.posts.post', post_id=post.id)}
        )

    @classmethod
    def get(cls):
        return {'blog_posts': [
            {'title': 'Random Title'},
            {'title': 'another Title'}
        ]}


class Post(Resource):
    @classmethod
    def get(cls, post_id):
        post = PostModel.find_by_id(post_id)
        if not post:
            return {'message': 'Post not found.'}, 404

        return post_schema.dump(post), 200

    @classmethod
    def put(cls, post_id):
        return {'title': 'Random Title', '': datetime.datetime.now()}, 204

    @classmethod
    def delete(cls, post_id):
        return {'title': 'Random Title', '': datetime.datetime.now()}, 204


blog_posts_api = Blueprint('resources.blog_posts', __name__)
api = Api(blog_posts_api)
api.add_resource(
    PostList,
    '/posts',
    endpoint='posts'
)
api.add_resource(
    Post,
    '/posts/<int:post_id>',
    endpoint='post'
)