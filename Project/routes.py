import datetime
import csv ,os,json
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL


mysql = MySQL()
routes = Blueprint('routes', __name__)



@routes.route('/')
def index():
	return render_template('welcome.html')

@routes.route('/dashboard')
def dashboard():
	if 'Uid' in session.keys():
		return render_template('welcome.html')
	else:
		return render_template('login.html')



@routes.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		cur = mysql.connection.cursor()
		cur.execute("SELECT * FROM users WHERE email = %s", (email,))
		user = cur.fetchone()
		cur.close()
		if user and check_password_hash(user[1], password):  # Access the password using index 1
			session['email'] = user[0]
			flash('Login successful!')
			return render_template('welcome.html')
		else:
			flash('Invalid credentials. Please try again.')
			return render_template('login.html')
	return render_template('login.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        firstName = request.form['first_name']
        lastName = request.form['last_name']
        email = request.form['email']
        password = request.form['password']


        if not firstName or not lastName or not email or not password:
            flash('All fields are required!', 'error')
            return render_template('signup.html')
        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'error')
            return render_template('signup.html')

        hashed_password = generate_password_hash(password)

        try:
            cur = mysql.connection.cursor()
            
            # Check if email already exists
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            if user:
                flash('Email is already registered. Please log in.', 'error')
                return render_template('signup.html')

            # Insert the new user into the database
            cur.execute(
                "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (firstName, lastName, email, hashed_password)
            )
            mysql.connection.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('routes.login'))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')
        finally:
            cur.close()
    return render_template('signup.html')

@routes.route('/logout')
def logout():
	session.pop('email', None)
	session.pop('name', None)
	session.pop('id', None)
	flash('You have been logged out.')
	return redirect(url_for('routes.login'))

@routes.route('/test_db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES;")
        tables = cur.fetchall()
        cur.close()
        return f"Connected! Tables: {tables}"
    except Exception as e:
        return f"Error: {str(e)}"

