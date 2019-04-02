import os
from flask import Blueprint, request, url_for, abort
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

from lib.image_helper import is_filename_safe, get_path
from models.post import PostModel
from lib.schemas import PostSchema
from resources.comments import CommentList

POST_NOT_FOUND = 'Post not found.'
INVALID_FILENAME = '{} is an invalid filename.'
IMAGE_NOT_FOUND = 'Could not remove the image at {}. Image not found.'

post_schema = PostSchema()
post_list_schema = PostSchema(many=True)


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
        page_num = request.args.get('page_num', 1)
        per_page = request.args.get('per_page', 10)
        try:
            page_num = int(page_num)
            per_page = int(per_page)
        except ValueError:
            return {'message': 'Make sure page_num and per_page are integers.'}, 400
        if per_page > 10:
            per_page = 10
        
        paginate = PostModel.page(page_num, per_page)
        return {
                'posts': post_list_schema.dump(paginate.items),
                'has_next': paginate.has_next,
                'has_prev': paginate.has_prev,
                'next_page': paginate.next_num,
                'prev_page': paginate.prev_num
            }


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

        user_id = get_jwt_identity()
        if not post.verify_post_author(user_id):
            abort(403)

        post.title = post_data.title
        post.category = post_data.category
        post.content = post_data.content
        # if image is updated must delete the prev one
        if post.image != post_data.image:
            folder = 'user_{}'.format(user_id)
            if not is_filename_safe(post_data.image):
                return {'message': INVALID_FILENAME.format(post_data.image)}, 400
            try:
                os.remove(get_path(filename=post.image, folder=folder))
                post.image = post_data.image
            except FileNotFoundError:
                return {'message': IMAGE_NOT_FOUND.format(post.image)}, 404
                

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

        user_id = get_jwt_identity()
        if not post.verify_post_author(user_id):
            abort(403)

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
    '/post/<int:post_id>',
    endpoint='post'
)
api.add_resource(
    CommentList,
    '/post/<int:post_id>/comments',
    endpoint='comments'
)