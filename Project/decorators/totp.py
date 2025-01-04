
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify

def totp_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is TOTP verified in the session
        if not session.get('totp_verified'):
            # If not verified, you can redirect or return JSON error
            flash("You must be TOTP-verified to perform this action.", "error")
            return redirect(url_for('user_bp.verify_totp_form'))  # or wherever
        return f(*args, **kwargs)
    return decorated_function
