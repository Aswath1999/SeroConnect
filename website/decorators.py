from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

# The check_confirmed decorator is used to check if the user's account is activated.
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.activation is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('auth.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function