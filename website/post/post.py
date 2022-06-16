from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from ..decorators import check_confirmed
from ..database.models import  Post
from .. import db

post=Blueprint('post',__name__)

@post.route('/post/<postid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def createpost(postid):
    post = Post.query.filter_by(id=postid).first()
    # post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    return 'success'

    # if request.method == 'POST':
    #     post = Post.query.filter_by(id=postid).first()
    #     if post:
    #         db.session.delete(post)
    #         db.session.commit()
    #         return redirect(url_for('views.forum'))
    #     else:
    #         print('no')
    # return f'<h1>hi {postid}</h1>'

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
   