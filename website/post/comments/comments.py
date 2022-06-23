from flask import Blueprint,render_template,request,redirect,url_for,jsonify
from flask_login import login_required,current_user
from ...decorators import check_confirmed
from ...database.models import  Post,User,Comment,Image
from ... import db
import json


comments=Blueprint('comments',__name__)

@comments.route('/comments/<postid>/<userid>',methods=['GET'])
@login_required
@check_confirmed
def show_comments(postid,userid):
    comments=Comment.query.filter(Comment.post_id==postid).all()
    owncomments=[]
    othercomments=[]
    for comment in comments:
        if comment.user_id==userid:
            owncomments.append(comment.text)

        else:
            othercomments.append(comment.text)
    return json.dumps({'usercomments':owncomments,'comments':othercomments})


@comments.route('/comments/create/<postid>/<userid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def createcomment(postid,userid):
    post = Post.query.filter_by(id=postid).first()
    if request.method == 'POST':
        text=request.form.get('comment')
        if text:
            comment = Comment(text=text,user_id=userid,post_id=postid)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('views.forum'))
        return redirect(url_for('views.forum'))
        

@comments.route('/comments/<commentid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def deletecomment(commentid):
    if request.method == 'POST':
        comment = Comment.query.filter_by(id=commentid).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return 'success'
        else:
            return "no posts found"
    else:
        return 'Failure'

@comments.route('/comment/edit/<commentid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def editcomment(commentid):
    comment = Comment.query.filter_by(id=commentid).first()
    if request.method == 'GET':
        return render_template('forum/editcomments.html',comment=comment,user=current_user)
    else:
        text=request.form.get('comment')
        comment.text=text
        db.session.commit()
        return redirect(url_for('views.forum'))
   
