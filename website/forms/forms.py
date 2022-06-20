from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField
from wtforms.validators import DataRequired,Email,EqualTo,Length


class SignupForm(FlaskForm):
    email=EmailField('Email address',validators=[DataRequired(),Email('This field requires a valid email address.')])
    Username=StringField('Enter your username',validators=[DataRequired()])
    password=PasswordField('Enter your password',validators=[DataRequired(),Length(min=4,max=15)])
    confirmpassword= PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password',message="Passwords must match")])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email=EmailField('Email address',validators=[DataRequired(),Email('This field requires a valid email address.')])
    password=PasswordField('Enter your password',validators=[DataRequired()])
    submit = SubmitField('Submit')

class ForgotForm(FlaskForm):
    email=EmailField('Email address',validators=[DataRequired(),Email('This field requires a valid email address.')])
    submit = SubmitField('Submit')

class ResetForm(FlaskForm):
    password=PasswordField('Enter your password',validators=[DataRequired(),Length(min=4,max=15)])
    submit = SubmitField('Submit')