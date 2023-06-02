from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash

followers_followed = db.Table( 
    'followers_followed',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary = followers_followed,
        primaryjoin = (followers_followed.columns.follower_id == id),
        secondaryjoin = (followers_followed.columns.followed_id == id),
        backref = db.backref('followers_followed', lazy='dynamic'),
        lazy='dynamic'
    )

    # hashes our password when user signs up
    def hash_password(self, signup_password):
        return generate_password_hash(signup_password)
    
    # This method will assign our columns with their respective values
    def from_dict(self, user_data):
        self.first_name = user_data['first_name']
        self.last_name = user_data['last_name']
        self.email = user_data['email']
        self.password = self.hash_password(user_data['password'])



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img_url = db.Column(db.String)
    title = db.Column(db.String(30))
    caption = db.Column(db.String(30))
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # This method will assign our columns with their respective values
    def from_dict(self, post_data):
        self.img_url = post_data['img_url']
        self.title = post_data['title']
        self.caption = post_data['caption']
        self.user_id = post_data['user_id']
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)