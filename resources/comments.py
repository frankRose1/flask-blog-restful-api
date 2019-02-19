from flask import Blueprint, request, url_for, abort
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.post import PostModel
from models.comment import CommentModel
from lib.schemas import CommentSchema
comment_schema = CommentSchema()

POST_NOT_FOUND = 'Post not found.'
COMMENT_NOT_FOUND = 'Comment not found.'


class CommentList(Resource):

    @classmethod
    @jwt_required
    def post(cls, post_id):
        post = PostModel.find_by_id(post_id)
        if not post:
            return {'message': POST_NOT_FOUND}, 404
        comment = comment_schema.load(request.get_json())
        user_id = get_jwt_identity()
        comment.author_id = user_id
        comment.post_id = post.id
        comment.save_to_db()
        
        return (
            '',
            201,
            {'Location': url_for('resources.posts.post', post_id=post.id)}
        )


class Comment(Resource):

    @classmethod
    def get(cls, comment_id):
        """Will fetch a single comment with the provided ID"""
        comment = CommentModel.find_by_id(comment_id)
        if not comment:
            return {'message': COMMENT_NOT_FOUND}, 404
        
        return {'comment': comment_schema.dump(comment)}


    @classmethod
    @jwt_required
    def put(cls, comment_id):
        """Update a comment with provided ID, check that user owns the comment"""
        comment_data = comment_schema.load(request.get_json())

        comment = CommentModel.find_by_id(comment_id)
        if not comment:
            return {'message': COMMENT_NOT_FOUND}, 404

        user_id = get_jwt_identity()
        if not comment.verify_comment_author(user_id):
            abort(403)

        comment.body = comment_data.body
        comment.save_to_db()
        return (
            '',
            204,
            {'Location': url_for('resources.comments.comment', comment_id=comment.id)}
        )

    @classmethod
    @jwt_required
    def delete(cls, comment_id):
        """Update a comment with provided ID, check that user owns the comment"""
        comment = CommentModel.find_by_id(comment_id)
        if not comment:
            return {'message': COMMENT_NOT_FOUND}, 404
        
        user_id = get_jwt_identity()
        if not comment.verify_comment_author(user_id):
            abort(403)

        comment.delete_from_db()
        return (
            '',
            204,
            {'Location': url_for('resources.posts.posts')}
        )


comments_api = Blueprint('resources.comments', __name__)
api = Api(comments_api)
api.add_resource(
    Comment,
    '/comment/<int:comment_id>',
    endpoint='comment'
)
