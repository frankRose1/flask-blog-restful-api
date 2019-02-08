from flask import Blueprint, request, url_for, abort
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.post import PostModel
from schemas.post import PostSchema

POST_NOT_FOUND = 'Post not found.'

post_schema = PostSchema()


def is_post_author(user_id, post):
    if user_id != post.author_id:
        abort(403)


class PostList(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        data = request.get_json()
        post = post_schema.load(data)
        user_id = get_jwt_identity()
        post.author_id = user_id
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

    @classmethod
    @jwt_required
    def put(cls, post_id):
        post_data = post_schema.load(request.get_json())

        post = PostModel.find_by_id(id=post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404

        is_post_author(get_jwt_identity(), post)

        post.title = post_data.title
        post.category = post_data.category
        post.content = post_data.content
        post.save_to_db()
        return (
            '',
            204,
            {'Location': url_for('resources.posts.post', post_id=post.id)}
        )

    @classmethod
    @jwt_required
    def delete(cls, post_id):
        post = PostModel.find_by_id(id=post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404

        is_post_author(get_jwt_identity(), post)

        post.delete_from_db()
        return (
            '',
            204,
            {"Location": url_for('resources.posts.posts')}
        )


posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)
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