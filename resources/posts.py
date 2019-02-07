from flask import Blueprint, request
from flask_restful import Resource, Api, url_for

from models.post import PostModel
from schemas.post import PostSchema
from marshmallow import ValidationError

POST_NOT_FOUND = 'Post not found.'

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
        return {'posts': [
            {'title': 'Random Title'},
            {'title': 'another Title'}
        ]}


class Post(Resource):
    @classmethod
    def get(cls, post_id):
        post = PostModel.find_by_id(post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404

        return {'post': post_schema.dump(post)}, 200

    # TODO check that author owns post
    @classmethod
    def put(cls, post_id):
        try:
            post_data = post_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        post = PostModel.find_by_id(id=post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404

        post.title = post_data.title
        post.category = post_data.category
        post.content = post_data.content
        post.save_to_db()
        return (
            '',
            204,
            {'Location': url_for('resources.posts.post', post_id=post.id)}
        )

    # TODO check that author owns it
    @classmethod
    def delete(cls, post_id):
        post = PostModel.find_by_id(id=post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404
        post.delete_from_db()
        return (
            '',
            204,
            {"Location": url_for('resources.posts.posts')}
        )


blog_posts_api = Blueprint('resources.posts', __name__)
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