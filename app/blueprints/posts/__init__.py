from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder='posts_templates', url_prefix='/posts')

from . import routes