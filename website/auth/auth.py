from flask import Blueprint,render_template,request,flash, url_for,redirect
from ..database.models import User
from .. import db
from flask_bcrypt import generate_password_hash,check_password_hash
from ..email.token import generate_confirmation_token, confirm_token
from ..email.mailer import send_email
from flask_login import (login_user, logout_user, login_required, current_user)
from ..forms.forms import SignupForm,LoginForm,ForgotForm,ResetForm

auth=Blueprint('auth',__name__)

# verifies login information of the user
@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                return render_template("auth/login.html", user=current_user,form=form)
        else:
            flash('Email does not exist.', category='error')
            return render_template("auth/login.html", user=current_user,form=form)
    return render_template("auth/login.html", user=current_user,form=form)


# returns new user's information to the database.
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form=SignupForm()
    if request.method == 'POST':
        if form.validate():
            username = form.Username.data  
            email = form.email.data
            password = form.password.data
            user= User.query.filter_by(email=email).first()
            if user:
                flash('Email already exists',category='error')
                return render_template('auth/signup.html',form=form,user=current_user)
            else:
                user = User(email=email, username=username, password=generate_password_hash(
                    password),activation=False)
                db.session.add(user)
                db.session.commit()

                token = generate_confirmation_token(user.email)
                confirm_url = url_for('auth.confirm_email', token=token, _external=True) #_external=True for absolute path
                html = render_template('auth/activate.html', confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(user.email, subject, html)
                    # login_user(new_user, remember=True)
                flash('Account created successfully',category='success')
                return redirect(url_for('auth.info'))
        errors = [{'field': key, 'messages': form.errors[key]} for key in form.errors.keys()] if form.errors else []
        return render_template('auth/signup.html',form=form,user=current_user,errors=errors)
    return render_template('auth/signup.html',form=form,user=current_user)
    
# returns sucess page on successful verification or registration
@auth.route('/confirmation')
def info():
    return render_template('auth/info.html',user=current_user)

# used to verify the user from the verification link sent to the user's email address.
@auth.route('/confirm/<token>')
def confirm_email(token):
    try:    
        email=confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.activation:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.activation = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('views.home'))

# Logs out the user
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# returns unconfirmed page when the user's account is not activated
@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.activation:
        return redirect(url_for('views.home'))
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html',user=current_user)

# to resend confirmation email to the user
@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('auth/activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    flash('A new confirmation email has been sent.', 'success')
    return redirect(url_for('auth.unconfirmed'))

# To change passwords and send password reset link.
@auth.route('/forgot',methods=['GET','POST'])
def forgot():
    form=ForgotForm()

    if request.method == 'POST' and form.validate_on_submit:
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        if user:
            token=generate_confirmation_token(user.email)
            db.session.commit()
            reset_url = url_for('auth.resetpass', token=token, _external=True)
            html=render_template('auth/resetpassword/reset.html',username=user.email,reset_url=reset_url,user=current_user)
            subject = "Reset your password"
            send_email(user.email, subject, html)
            return redirect(url_for("auth.info"))
        else:
            flash('The email doesnot exist.', 'error')
            return render_template('auth/resetpassword/forgot.html',user=current_user,form=form)
    return render_template('auth/resetpassword/forgot.html',user=current_user,form=form)

# Resets the password from the link sent to the user.
@auth.route('/resetpass/<token>', methods=['GET', 'POST'])
def resetpass(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    form=ResetForm()
    if user:
        if request.method =='POST':
            user = User.query.filter_by(email=email).first()
            if user:
                user.password=generate_password_hash(form.password.data)
                db.session.commit()
                login_user(user)
                print('Sucess')
                return redirect(url_for('views.home'))
            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('auth.login'))

        else:
            flash('You can now change your password.', 'success')
            return render_template('auth/resetpassword/resetpass.html',user=current_user,form=form)
    else:
        flash('Can not reset the password, try again.', 'danger')

    return redirect(url_for('views.home'),user=current_user)