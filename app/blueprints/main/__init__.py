from flask import Blueprint
bp = Blueprint('main', __name__, url_prefix='/')

from .import models, views # . means from current directory = app.blueprints.main
