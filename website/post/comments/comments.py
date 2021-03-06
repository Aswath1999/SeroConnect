from flask import Blueprint,render_template,request,redirect,url_for,jsonify
from flask_login import login_required,current_user
from ...decorators import check_confirmed
from ...database.models import  Post,User,Comment,Image
from ... import db
import json


comments=Blueprint('comments',__name__)

@comments.route('/comments/<postid>',methods=['GET'])
@login_required
@check_confirmed
def show_comments(postid):
    page=request.args.get('page',1,type=int)
    comments=Comment.query.filter(Comment.post_id==postid).order_by(Comment.date.desc()).paginate(page=page,per_page=3)
    post=Post.query.filter_by(id=postid).first()
    if "hx_request"  in request.headers:
        return render_template("forum/showcomments.html",comments=comments,postuser=User,user=current_user,post=post,postimage=Image)
    return render_template("forum/comments.html",comments=comments,postuser=User,user=current_user,post=post,postimage=Image)
    
    
@comments.route('/comments/create/<postid>/<userid>',methods=['GET', 'POST'])
@login_required
@check_confirmed
def createcomment(postid,userid):
    post = Post.query.filter_by(id=postid).first()    
    text=json.loads(request.data).get('data')
    if text:
        comment = Comment(text=text,user_id=userid,post_id=postid)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'success':'sucess'})

        

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
        return redirect(url_for('comments.show_comments',postid=comment.post_id,userid=current_user.id))
   
