from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    username=db.Column(db.String(150))
    date=db.Column(db.DateTime(timezone=True), default=func.now())
    activation=db.Column(db.Boolean,nullable=False,default=False)
