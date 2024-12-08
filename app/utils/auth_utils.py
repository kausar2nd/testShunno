from flask import session, flash, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "loggedin" not in session:
            flash("Please log in to access this page.")
            return redirect(url_for("general.all_login"))
        return f(*args, **kwargs)

    return decorated_function
