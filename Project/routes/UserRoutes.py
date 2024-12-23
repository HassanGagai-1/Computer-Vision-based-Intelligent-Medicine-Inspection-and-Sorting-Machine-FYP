from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from services.UserService import UserService
from flask import render_template
import logging
logger = logging.getLogger(__name__)
user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
def home():
    return render_template('signup.html')

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    
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
        # data = request.get_json()
        firstname = request.form.get('firstname')   
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        # Register user via service
        
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
        return render_template('login.html', error='Invalid email or password'), 400

    try:
        user = UserService.login_user(email, password)
        session.permanent = True
        session['user_id'] = user.id
        return redirect('/dashboard')
    except ValueError as e:
        return render_template('login.html', error=str(e)), 400
    
@user_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')
