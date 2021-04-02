from flask import Blueprint

#RESTful 

bp = Blueprint('auth', __name__, url_prefix='/auth') #making a auth directory to contain all auth packages 

#tell bp app to use all views associated with bp
from app.blueprints.auth import views, models  