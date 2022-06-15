from flask import Blueprint,render_template,request,flash, url_for,redirect
from ..database.models import User
from .. import db
from flask_bcrypt import generate_password_hash,check_password_hash
from ..email.token import generate_confirmation_token, confirm_token
from ..email.mailer import send_email
from flask_login import (login_user, logout_user, login_required, current_user)

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                print('Error')
        else:
            flash('Email does not exist.', category='error')
            print('Error')

    return render_template("auth/login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        username = request.form.get('Username')  
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user= User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User(email=email, username=username, password=generate_password_hash(
                password1),activation=False)
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

    return render_template('auth/signup.html',user=current_user)

@auth.route('/confirmation')
def info():
    return render_template('auth/info.html')

@auth.route('/confirm/<token>')
def confirm_email(token):
    try:    
        email=confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        print('dangert')
    user = User.query.filter_by(email=email).first_or_404()
    if user.activation:
        flash('Account already confirmed. Please login.', 'success')
        print('confirmed')
    else:
        user.activation = True
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('auth.info'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.activation:
        return redirect(url_for('views.home'))
    flash('Please confirm your account!', 'warning')
    return render_template('auth/unconfirmed.html')

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


@auth.route('/forgot',methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email=request.form.get('email')
        user=User.query.filter_by(email=email).first()
        token=generate_confirmation_token(user.email)
        db.session.commit()
        reset_url = url_for('auth.resetpass', token=token, _external=True)
        html=render_template('auth/resetpassword/reset.html',username=user.email,reset_url=reset_url)
        subject = "Reset your password"
        send_email(user.email, subject, html)
        flash('A password reset email has been sent via email.', 'success')
        return redirect(url_for("auth.login"))
    return render_template('auth/resetpassword/forgot.html')

@auth.route('/resetpass/<token>', methods=['GET', 'POST'])
def resetpass(token):
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()

    if user:
        if request.method =='POST':
            user = User.query.filter_by(email=email).first()
            if user:
                user.password=generate_password_hash(request.form.get('password'))
                db.session.commit()
                login_user(user)
                print('Sucess')
                flash('Password successfully changed.', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Password change was unsuccessful.', 'danger')
                return redirect(url_for('auth.login'))

        else:
            flash('You can now change your password.', 'success')
            return render_template('auth/resetpassword/resetpass.html')
    else:
        flash('Can not reset the password, try again.', 'danger')

    return redirect(url_for('views.home'))