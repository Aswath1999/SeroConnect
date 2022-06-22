from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


basedir=path.abspath(path.dirname(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"

app=Flask(__name__)
app.secret_key=app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)
# Image upload
UPLOAD_FOLDER='static/images/'
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2*1024*1024*10
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']

    
from .views import views
from .auth.auth import auth
from .post.post import post
from .post.comments.comments import comments

app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(post, url_prefix='/')
app.register_blueprint(comments, url_prefix='/')



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

create_database(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .database.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# bcrypt = Bcrypt(app)

