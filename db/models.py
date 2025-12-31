from . import db
from flask_login import UserMixin

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(162), nullable = False)

class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)

class gifts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    gift_number = db.Column(db.Integer, nullable=False)  
    is_opened = db.Column(db.Boolean, default=False)
    opened_at = db.Column(db.DateTime)
    position_data = db.Column(db.Text, nullable=False)
    auth_only = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'gift_number', name='unique_user_gift'),)