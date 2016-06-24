from flask import Blueprint

# main = Blueprint('main', __name__, template_folder='pages')
main = Blueprint('main', __name__)


from . import views


