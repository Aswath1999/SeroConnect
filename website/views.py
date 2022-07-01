from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .decorators import check_confirmed
from .database.models import Post,User,Comment,Image
from . import db
from website import app
from .post.images import createuserimage,deleteuserimage




views=Blueprint('views',__name__)


# returns the home page
@views.route('/',methods=['GET', 'POST'])
def home():
    return render_template("home.html",user=current_user)

#the decorators login_required and check_confirmed is used to check whether the user is logged in and activated
#returns the forum page with pagination of posts and infinite scrolling.
@views.route('/forum',methods=['GET', 'POST'])
@login_required
@check_confirmed
def forum():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=4) # The paginate from flask helps us to not load all posts from the database at once.
    if "hx_request"  in request.headers:  #hx_request is from the htmx library and is used for activating infinite scroll
        return render_template("forum/viewpost.html",user=current_user,postuser=User,posts=posts,postcomment=Comment,postimage=Image)
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=posts,postcomment=Comment,postimage=Image)

#Profile page of user with pagination of user's posts
@views.route('/userprofile',methods=['GET', 'POST'])
@login_required
@check_confirmed
def userprofile():
    page=request.args.get('page',1,type=int)
    posts=Post.query.filter(Post.user_id==current_user.id).paginate(page=page,per_page=4)
    if "hx_request"  in request.headers:
        return render_template("forum/viewpost.html",user=current_user,postuser=User,posts=posts,postcomment=Comment,postimage=Image)
    return render_template('profile.html',user=current_user,posts=posts,postuser=User,postcomment=Comment,postimage=Image)


# Get and update user's profile information
@views.route('/profileupdate',methods=['GET', 'POST'])
@login_required
@check_confirmed
def profileinfo():
    if request.method == 'GET':
        return render_template('profileinfoupdate.html',user=current_user)
    else:
        page=request.args.get('page',1,type=int)
        posts=Post.query.filter(Post.user_id==current_user.id).paginate(page=page,per_page=4)
        user=User.query.filter_by(id=current_user.id).first()
        Username=request.form.get('Username')
        image=request.files['file']
        username=User.query.filter_by(username=Username).first()
        if username:
            flash('Username already exists', category='error')
            return render_template("profileinfoupdate.html",user=current_user)
        else:
            user.username=Username
            db.session.commit()
            if image:
                deleteuserimage(user.id)
                filename=createuserimage(image,user.id)
                user.image=filename
                db.session.commit()
                return render_template('profile.html',user=current_user,posts=posts,postuser=User,postcomment=Comment,postimage=Image)
            return render_template('profile.html',user=current_user,posts=posts,postuser=User,postcomment=Comment,postimage=Image)

@views.route('/podcast',methods=['GET'])
@login_required
@check_confirmed
def podcast():
    return render_template('podcast.html',user=current_user)
        
            


