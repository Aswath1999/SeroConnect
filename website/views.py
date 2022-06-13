from flask import Blueprint,render_template
from flask_login import login_required,current_user
from .decorators import check_confirmed

views=Blueprint('views',__name__)


@views.route('/')
@login_required
@check_confirmed
def home():
    return render_template("home.html",user=current_user)
