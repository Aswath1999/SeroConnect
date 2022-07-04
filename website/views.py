from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from .decorators import check_confirmed
from .database.models import Post,User,Comment,Image,Video
from . import db
from website import app
from .post.images import createuserimage,deleteuserimage,createvideo,deletevideo




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
            flash('Username already exists', category='success')
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

@views.route('/podcast',methods=['GET','POST'])
@login_required
@check_confirmed
def podcast():
    page=request.args.get('page',1,type=int)
    videos=Video.query.order_by(Video.date.desc()).paginate(page=page,per_page=4)
    if "hx_request"  in request.headers:
        return render_template("viewpodcast.html",user=current_user,videos=videos)
    return render_template('podcast.html',user=current_user,videos=videos)
        
@views.route('/podcastupload',methods=['GET','POST'])
@login_required
@check_confirmed
def uploadpodcast():
    if request.method == 'POST':
        video=request.files['file']
        filename=createvideo(video)
        if filename:
            Title=request.form.get('Title')
            content=request.form.get('content')
            video=Video(title=Title,content=content,video=filename)
            db.session.add(video)
            db.session.commit()
            flash('Video/Audio uploaded successfully','success')
            return redirect(url_for('views.podcast'))
        else:
            flash('error uploading video/Audio','error')
            return redirect(url_for('views.podcast'))
    return render_template('podcastupload.html',user=current_user)
        
            
@views.route('/podcastdelete/<videoid>',methods=['GET','POST'])
@login_required
@check_confirmed
def deletepodcast(videoid):
    if request.method == 'POST':
        video = Video.query.filter_by(id=videoid).first()
        if video:
            deletevideo(video.id)
            db.session.delete(video)
            db.session.commit()
            return 'success'
        else:
            return "no posts found"
    else:
        return 'Failure'