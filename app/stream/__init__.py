from flask import Blueprint

stream = Blueprint('stream', __name__)

from . import routes
