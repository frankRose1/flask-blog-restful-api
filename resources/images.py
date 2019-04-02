import os
import traceback
from flask import Blueprint, request, send_file
from flask_restful import Resource, Api
from flask_uploads import UploadNotAllowed
from flask_jwt_extended import jwt_required, get_jwt_identity

from lib import image_helper
from lib.schemas import ImageSchema

image_schema = ImageSchema()

class ImageUpload(Resource):

    @jwt_required
    def post(self):
        """Used to upload an image.
            Each user will have their own folder. If there is a name conflict
            append a number to the end.
        """
        data = image_schema.load(request.files) # {"image": FileStorage}
        user_id = get_jwt_identity()
        folder = f'user_{user_id}' # static/images/user_1/
        try:
            image_path = image_helper.save_image(image=data['image'], folder=folder)
            basename = image_helper.get_basename(image_path)
            return {'image': f'{request.url_root[:-1]}/static/images/{image_path}', 'message': f'Image {basename} has been uploaded.' }, 201
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {'message': f'The extension "{extension}" is not allowed.'}, 400


class Image(Resource):
    def get(self):
        """Returns the requested image if it exists"""
        pass

    def delete(self):
        pass


images_api = Blueprint('resources.images', __name__)
api = Api(images_api)
api.add_resource(
    ImageUpload,
    '/images/upload',
    endpoint='image_upload'
)
