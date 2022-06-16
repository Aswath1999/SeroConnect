from .. import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    username=db.Column(db.String(150))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    activation=db.Column(db.Boolean,nullable=False,default=False)
    Post = db.relationship("Post", back_populates="owner")

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner=db.relationship('User',back_populates='Post')