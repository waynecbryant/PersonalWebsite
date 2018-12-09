#models.py
from blogresume import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_manager
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True) #makes column an index that can be used
    password_hash = db.Column(db.String(128))
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.username = username
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password)

    def check_password(self, password):
        return Bcrypt().check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username: {self.username}"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id
    
    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} -- Title: {self.title}"