from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from ..decorators import check_confirmed
from ..database.models import  Post,User,Image,Comment
from werkzeug.utils import secure_filename
from .. import db,basedir
from website import app
import uuid as uuid
import os



post=Blueprint('post',__name__)



@post.route('/post/<postid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def deletepost(postid):
    if request.method == 'POST':
        post = Post.query.filter_by(id=postid).first()
        if post:
            deleteimage(postid)
            db.session.delete(post)
            db.session.commit()
            return 'success'
        else:
            return "no posts found"
    else:
        return 'Failure'

@post.route('/post/edit/<postid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def editpost(postid):
    post = Post.query.filter_by(id=postid).first()
    if request.method == 'GET':
        return render_template('forum/editpost.html',post=post,user=current_user)
    else:
        content=request.form.get('content')
        title=request.form.get('Title')
        post.content=content
        post.title=title

        db.session.commit()
        return redirect(url_for('views.forum'))


   
@post.route('/anonymous',methods=['GET', 'POST'])
@login_required
@check_confirmed
def anonymous():
    post=Post.query.all()
    if request.method == 'POST':
        title=request.form.get('Title')
        content=request.form.get('content')
        post = Post(title=title, content=content,user_id=current_user.id,anonymous=True)
        db.session.add(post)
        db.session.commit()
        db.session.add(post)
        db.session.commit()
        postid=post.id
        files = request.files.getlist("file")
        if files:
            for file in files:
                filename=secure_filename(file.filename)
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    return f'Invalid image{filename}', 400
                else:
                    filename=str(uuid.uuid1())+"_"+filename
                    file.save(os.path.join(basedir,app.config['UPLOAD_FOLDER'],filename))
                    image=Image(image=filename,post_id=postid)
                    db.session.add(image)
                    db.session.commit()
            return redirect(url_for('views.forum'))
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=post,postcomment=Comment,postimage=Image)


def deleteimage(postid):
    images=Image.query.filter(Image.post_id==postid).all()
    if images:
        for image in images:
            os.remove(os.path.join(basedir,app.config['UPLOAD_FOLDER'],image.image))