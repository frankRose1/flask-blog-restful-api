"""
  Contains functions that help to save, retrieve, and delete images
"""
import os
import re
from werkzeug.datastructures import FileStorage
from typing import Union
from flask_uploads import IMAGES, UploadSet

# will create a folder in static/ called images
# IMAGES sets the file types that are accepted(jpg, png, svg, etc)
IMAGE_SET = UploadSet('images', IMAGES)

def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Saves FileStorage to a folder"""
      return IMAGE_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Returns the full path to an image"""
      return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union(str, None):
    """Takes a filename and returns an image with any of the accepted formats 
      if it exists
    """
    for _format in IMAGES:
        image = '{}.{}'.format(filename, _format)
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        # check whether the given path is a file
        if os.path.isfile(image_path):
            return image_path
        return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Takes a FileStorage or string and returns the file name. Allows other 
      helper functions to call this with either FileStorage or filename strings
      and will always return the file name.
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_basename(file: Union[str, FileStorage]) -> str:
    """Return full name of image in a path
      get_basename(some/folder/image.jpg) --> image.jpg
    """
    filename = _retrieve_filename(file)
    # split will split at the final part of the path(image.jpg) and everything
    #  before it is at index 0
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
  """Return the extension of an image file
      get_extension(image.jpg) --> .jpg
    """
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """Check a regex and return if string matches or not"""
    filename = _retrieve_filename(file)
    accpeted_formats = '|'.join(IMAGES) #png|jpg|svg|jpeg
    # start with any of alphanumeric, follwed by alhpanumeric and special characters(any amount), ".", then one of the accepted formats
    regex = f'[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({accepted_formats})$'
    #  if no match is found match() returns None
    return re.match(filename, regex) is not None