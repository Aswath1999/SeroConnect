from flask_mail import Message,Mail
from website import app

mail= Mail(app)

# sends verification email to the user's registered email address.
def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)