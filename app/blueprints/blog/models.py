#flask-SQL alchemy object relational mapper 
from app import db #import our database instance 
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text) # unfiltered, unbridled string, no characters limit 
    date_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    date_update = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False) #reference the post class in lower case first (consistent with SQLAlchemy), then column 


    def __repr__(self):
        return f'<Post: ID: [{self.id}] {self.body[14]}...>'

