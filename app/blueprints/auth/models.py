from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.blueprints.blog.models import Post
# from sqlalchemy.dialects.postgresql import UUID
# import shortuuid

# [id, a, b]
# [1, 1, 5 ]
# [2, 3, 1 ]
# [3, 3, 2 ]

#creating a table with sqlalchemy, not flask-sqlalchemy
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')), #ppl who follow me
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')) #ppl who I follow 
)


class User(UserMixin, db.Model): #inheriting funcs(Model class) from flask-sqlalchemy to build out data model
    id = db.Column(db.Integer, primary_key=True, unique=True) #default=shortuuid.ShortUUID(alphabet='1234567890').random(length=6), 
    first_name = db.Column(db.String)
    last_name = db.Column(db.String) 
    email = db.Column(db.String, unique=True) # how the data/object relates to DB table column 
    password = db.Column(db.String)
    posts = db.relationship('Post', cascade='all, delete-orphan', backref='user', lazy=True) # creating a foreign key, "post of xx user". lazy: won't show up until we specifically retrieve it 
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id), #.c relating two tables together
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )

    def __init__(self, first_name, last_name, email, g_auth_verify = False, password = ''): #handling logic of instance/object creation, always use __init__to instantiate object   
        super().__init__() #inherit all the functionality from Model class 
        self.first_name = first_name #set attributes to be whatever passing 
        self.last_name = last_name
        self.password = password
        self.email = email
        self.g_auth_verify = g_auth_verify

    def followed_posts(self):
        followed = Post.query.join(
            followers,
            (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id) #posts all people I'm following
        self_posts = Post.query.filter_by(user_id=self.id) #my own posts 
        all_posts = followed.union(self_posts).order_by(Post.date_created.desc())
        db.session.commit()
        return all_posts

    #fro following functionality
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    #when user register...
    def create_password_hash(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password_hash(self, password_to_verify):
        return check_password_hash(self.password, password_to_verify)

    def save(self):
        self.create_password_hash(self.password)
        db.session.add(self)
        db.session.commit()

    #whenever user login...taking user object info, store it in session  

    def __repr__(self):
        return f'<User: {self.email}>'

    #once a user loged in, set the info in session to support cross page refreshes 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)