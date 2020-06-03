import hashlib
from functools import wraps
from flask import session, flash, redirect, url_for


def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def wrap(args, **kwargs):
        if 'logged_in' in session:
            return f(args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
