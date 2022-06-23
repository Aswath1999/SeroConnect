from flask import Blueprint,render_template,request
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
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.date.desc()).paginate(page=page,per_page=4)
    if "hx_request"  in request.headers:
        return render_template("forum/viewpost.html",user=current_user,postuser=User,posts=posts,postcomment=Comment,postimage=Image)
    return render_template("forum/forum.html",user=current_user,postuser=User,posts=posts,postcomment=Comment,postimage=Image)