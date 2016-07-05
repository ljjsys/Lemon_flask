from flask import Blueprint

data_sync = Blueprint('data_sync', __name__)

from . import views