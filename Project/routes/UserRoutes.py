from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from werkzeug.security import generate_password_hash
from services.UserService import UserService
from flask import render_template

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard', methods=['GET'])
def index():
	return render_template('dashboard.html')


@user_bp.route('/register', methods=['POST','GET'])
def register():
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
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return render_template('login.html', error='Invalid email or password'), 400

    try:
        user = UserService.login_user(request.form.get('email'), request.form.get('password'))
        return redirect('/dashboard')
    except ValueError as e:
        return render_template('login.html', error=str(e)), 400
