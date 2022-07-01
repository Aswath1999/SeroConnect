from itsdangerous import URLSafeTimedSerializer
from website import app

app.config.from_pyfile('config.py')

# Generates unique token for the registered email address.
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# Checks whether the token matches when user clicks the verification email.
def confirm_token(token,expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email