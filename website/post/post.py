from flask import Blueprint,render_template,request,redirect,url_for,make_response,jsonify
from flask_login import login_required,current_user
from ..decorators import check_confirmed
from ..database.models import  Post,User,Image,Comment
from .images import createimage,deleteimage
from .. import db
from website import app



post=Blueprint('post',__name__)
# To create posts and saves to database
@post.route('/forum/post',methods=['GET', 'POST'])
@login_required
@check_confirmed
def createpost():
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
    else:
        return render_template('forum/createpost.html',user=current_user)

# Deletes posts asyncronously with the help of AJAX requests
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

# Edits information on the posts
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
        files = request.files.getlist("file")
        post.content=content
        post.title=title
        deleteimage(postid)
        createimage(files,postid)
        db.session.commit()
        return redirect(url_for('views.forum'))


#  the anonymous function is used to create posts anonymously  
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
        createimage(files,postid)
        return redirect(url_for('views.forum'))
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=post,postcomment=Comment,postimage=Image)
