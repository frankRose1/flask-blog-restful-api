from flask import Blueprint, request, url_for, abort
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.post import PostModel
from models.user import UserModel
from models.comment import CommentModel

from schemas import CommentSchema
comment_schema = CommentSchema()
COMMENT_NOT_FOUND = 'Comment not found.'



class CommentList(Resource):

    @classmethod
    @jwt_required
    def post(cls, post_id):
        comment = comment_schema.load(request.get_json())
        user_id = get_jwt_identity()
        comment.author_id = user_id
        comment.save_to_db()
        
        return (
            '',
            201,
            {'Location': url_for('resources.comments.comment', comment_id=comment.id)}
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

        comment = Comment.find_by_id(comment_id)
        if not comment:
            return {'message': COMMENT_NOT_FOUND}, 404

        user_id = get_jwt_identity()
        if not comment.check_comment_author(user_id):
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
        if not comment.check_comment_author(user_id):
            abort(403)

        comment.delete_from_db()
        return (
            '',
            204,
            {'Location': url_for('resources.comments.comments')}
        )


comments_api = Blueprint('resources.comments', __name__)
api = Api(comments_api)
api.add_resource(
    CommentList,
    '/comments',
    endpoint='comments'
)
api.add_resource(
    Comment,
    '/comments/<int:comment_id>',
    endpoint='comment'
)
