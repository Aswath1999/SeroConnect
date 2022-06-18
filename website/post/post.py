from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from ..decorators import check_confirmed
from ..database.models import  Post,User
from .. import db

post=Blueprint('post',__name__)

@post.route('/post/<postid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def deletepost(postid):
    if request.method == 'POST':
        post = Post.query.filter_by(id=postid).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return 'success'
        else:
            return "no posts found"
    else:
        return 'Failure'

    # if request.method == 'POST':
    #     post = Post.query.filter_by(id=postid).first()
    #     if post:
    #         db.session.delete(post)
    #         db.session.commit()
    #         return redirect(url_for('views.forum'))
    # return redirect(url_for('views.forum'))

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
        return redirect(url_for('views.forum'))
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=post)