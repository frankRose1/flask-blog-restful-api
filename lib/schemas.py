from . ma import ma
from models.post import PostModel
from models.user import UserModel
from models.comment import CommentModel


class PostSchema(ma.ModelSchema):
    author = ma.Nested('UserSchema', only=['username'])
    comments = ma.Nested('CommentSchema', many=True, only=['body', 'author', 'created_date'])
    class Meta:
        model = PostModel
        # load_only will not be dumped
        # dump_only will not be validated on load
        dump_only = ('id', 'created_on')
        include_fk = True


class UserSchema(ma.ModelSchema):
    posts = ma.Nested(PostSchema, many=True, only=['title', 'id', 'created_on'])
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id',)


class CommentSchema(ma.ModelSchema):

    author = ma.Nested(UserSchema, only=['username'])
    post = ma.Nested(PostSchema, only=['id', 'title'])

    class Meta:
        model = CommentModel
        dump_only = ('id', 'created_date')
        include_fk = True