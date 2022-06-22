from flask import Blueprint,render_template,request,redirect, url_for,abort
from flask_login import login_required,current_user
from .decorators import check_confirmed
from .database.models import Post,User,Comment,Image
from . import db
from website import app
from .post.images import createimage,deleteimage




views=Blueprint('views',__name__)


@views.route('/',methods=['GET', 'POST'])
def home():
    return render_template("home.html",user=current_user)


@views.route('/forum',methods=['GET', 'POST'])
@login_required
@check_confirmed
def forum():
    post=Post.query.all()
    if request.method == 'POST':
        title=request.form.get('Title')
        content=request.form.get('content')
        post = Post(title=title, content=content,user_id=current_user.id,anonymous=False)
        db.session.add(post)
        db.session.commit()
        postid=post.id
        files = request.files.getlist("file")
        createimage(files,postid)
        return redirect(url_for('views.forum'))
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=post,postcomment=Comment,postimage=Image)
    
