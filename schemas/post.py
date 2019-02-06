from ma import ma
from models.post import PostModel


class PostSchema(ma.ModelSchema):
    class Meta:
        model = PostModel
        # load_only will not be dumped
        # dump_only will not be validated on load
        dump_only = ('id', 'created_on')
