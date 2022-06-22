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
    Post = db.relationship("Post", back_populates="owner",cascade='delete')

class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    anonymous=db.Column(db.Boolean,nullable=False,default=False)
    owner=db.relationship('User',back_populates='Post')
    comments=db.relationship('Comment',back_populates='post',cascade='delete')
    image=db.relationship('Image',back_populates='post',cascade='delete')

class Image(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    image=db.Column(db.String(150))
    post=db.relationship('Post', back_populates='image')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    
class Comment(db.Model):
    __tablename__='comments'
    id = db.Column(db.Integer, primary_key=True)
    text= db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship("Post", back_populates="comments")
