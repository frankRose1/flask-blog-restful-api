from ma import ma
from models.post import PostModel
from schemas.user import UserSchema


class PostSchema(ma.ModelSchema):
    author = ma.Nested(UserSchema)

    class Meta:
        model = PostModel
        # load_only will not be dumped
        # dump_only will not be validated on load
        dump_only = ('id', 'created_on')
        include_fk = True
