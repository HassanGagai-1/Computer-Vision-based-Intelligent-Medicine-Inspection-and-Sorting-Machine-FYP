from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from services.UserService import UserService
from flask import render_template
from models.users import User
import logging
from extensions import db
from services.totp_service import generate_totp_secret, get_totp_uri, generate_qr_code_image,verify_totp_code
import datetime


logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def home():
    return render_template('signup.html')

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    print("Current session:", session)
    if 'user_id' not in session:
        return redirect('/login')
    else:
	    return render_template('dashboard.html')

@user_bp.route('/register', methods=['POST','GET'])
def register():
    logger.debug("UserRoutes.register endpoint called")
    if request.method == 'GET':
        return render_template('signup.html')
    try:
        firstname = request.form.get('firstname')   
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        
        UserService.register_user(firstname, lastname, email, password)
        return redirect('/login')
    except ValueError as e:
        return render_template('signup.html', error=str(e)), 400

@user_bp.route('/login', methods=['POST','GET'])
def login():
    logger.debug("UserRoutes.login endpoint called")
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    logger.info('User login attempt')

    if not email or not password:
        flash('Invalid email or password', 'error')
        return render_template('login.html', error='Invalid email or password'), 400

    try:
        user = UserService.login_user(email, password)
        session.permanent = True
        session['user_id'] = user.id
        return redirect('/dashboard')
    except ValueError:
        flash('Invalid credentials', 'error')
        return render_template('login.html', error='Invalid email or password'), 400

@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash("You have been successfully logged out!", "Info")
    return redirect('/login')

@user_bp.route("/api/forget-password", methods=['GET', 'POST'])
def forget_password():
    logger.debug("Forget Password API called")
    if request.method == 'GET':
        return render_template('forget-password.html')
    if request.method == 'POST':
        email = request.form.get('email')
        UserService.forget_password(email)
        
        flash('Password reset instructions have been sent to your email.', 'password_reset')
        return render_template('forget-password.html')

@user_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if user and user.reset_token_expiry > datetime.datetime.now():
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            UserService.reset_password(user, new_password)
            
            flash('Your password has been successfully reset.', 'success')
            return redirect('/login')
        
        return render_template('reset_password.html')
    
    flash('The reset link is invalid or has expired.', 'error')
    return redirect(url_for('user.forgot_password'))




@user_bp.route('/api/getUserProfile', methods=['GET']) 
def getUserProfile():
    current_user_id = session.get('user_id')
    logger.debug(f"Current user id: {current_user_id}")
    if not current_user_id:
        return jsonify({"error": "Unauthorized access"}), 401

    User = UserService.get_user_profile(current_user_id)
    
    if User:
        return jsonify(User.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404


@user_bp.route('/profile', methods=['GET'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    user = User.query.get(user_id)
    return render_template('profile.html')

@user_bp.route('/enable_totp/<int:user_id>', methods=['POST','GET'])
def enable_totp(user_id):
    """Admin route to enable TOTP for a user and return a QR code for scanning."""
    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")
    
    # Generate a new secret and store it
    secret = generate_totp_secret()
    user.totp_secret = secret
    db.session.commit()

    # Create the TOTP URI
    totp_uri = get_totp_uri(secret, user.firstname, issuer='MyApp')

    # Optional: Generate a QR code image in memory
    qr_buf = generate_qr_code_image(totp_uri)

    # Return the image as a response so admin can show it to the user
    # or save it somewhere
    return send_file(qr_buf, mimetype='image/png')


@user_bp.route('/verify_totp', methods=['POST'])
def verify_totp():
    """Route that verifies the TOTP code the user typed in."""
    user_id = session.get('user_id')  
    code = request.form.get('totp_code')

    user = User.query.get(user_id)
    if not user or not user.totp_secret:
        return jsonify({"error": "User not found or TOTP not enabled."}), 400

    if verify_totp_code(user.totp_secret, code):
        session['totp_verified'] = True
        flash("TOTP verification successful", "verified")
        return render_template('dashboard.html')
    else:
        flash("Invalid TOTP code", "TOTPError")
        return render_template('dashboard.html')

