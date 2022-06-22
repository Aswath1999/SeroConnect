from flask import Blueprint,render_template,request,redirect, url_for,abort
from flask_login import login_required,current_user
from .decorators import check_confirmed
from .database.models import Post,User,Comment,Image
from . import db,basedir
from website import app
import os
from werkzeug.utils import secure_filename
import uuid as uuid



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
        if files:
            for file in files:
                filename=secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    pass
                else:
                    filename=str(uuid.uuid1())+"_"+filename
                    file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'], filename))
                    image=Image(image=filename,post_id=postid)
                    db.session.add(image)
                    db.session.commit()
            return redirect(url_for('views.forum'))
        return render_template("forum/forum.html",user=current_user,postuser=User,posts=post,postcomment=Comment,postimage=Image)
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=post,postcomment=Comment,postimage=Image)
    
