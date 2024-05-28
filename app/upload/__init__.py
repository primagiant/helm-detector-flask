from flask import Blueprint

upload = Blueprint('upload', __name__)

from . import routes