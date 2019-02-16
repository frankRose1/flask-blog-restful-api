from flask import Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required 

from models.post import PostModel
from models.user import UserModel

class CommentList(Resource):

    @classmethod
    @jwt_required
    def post(cls, post_id):
        pass

    @classmethod
    def get(cls, post_id):
        """Return a list of comments that belong to a given post ID"""
        pass


class Comment(Resource):

    @classmethod
    def get(cls, comment_id):
        """Will fetch a single comment with the provided ID"""
        pass

    @classmethod
    @jwt_required
    def put(cls, comment_id):
        """Update a comment with provided ID, check that user owns the comment"""
        pass

    @classmethod
    @jwt_required
    def delete(cls, comment_id):
        """Update a comment with provided ID, check that user owns the comment"""
        pass


comments_api = Blueprint('resources.comments', __name__)
api = Api(comments_api)
api.add_resource(
    CommentList,
    '/comments',
    endpoint='comments'
)
api.add_resource(
    Comment,
    '/comments/<int:comment_id>'
    endpoint='comment'
)