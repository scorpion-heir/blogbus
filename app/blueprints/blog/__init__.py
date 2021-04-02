from flask import Blueprint

bp = Blueprint('blog', __name__, url_prefix='/blog') #I want be able to create, edit, delete post on my /blog page, then show them up on home page

from .import models, views 