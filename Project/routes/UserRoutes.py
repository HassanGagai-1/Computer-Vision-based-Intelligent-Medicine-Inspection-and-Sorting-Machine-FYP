from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session ,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import services.UserServices as userService


postgres = psycopg2.connect(database='postgres', user='postgres', password='12345', host='localhost', port='5432')
user_bp = Blueprint('users', __name__)

# @user_bp.route('/register', methods=['GET', 'POST'])
# def signup():
    


@user_bp.route('/user', methods=['GET'])
def get_notes():
    users = userService.get_all_users()
    users_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'email': user.email, 'password': user.password} for user in users]
    return jsonify({'notes': users_list})


@user_bp.route('/createUser', methods=['POST'])
def create_note_route():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    if not firstname or not lastname or not email or not password:
        return jsonify({'error': 'Name and description are required'}), 400

    new_user_id = insert_user(firstname, lastname, email, password)
    return jsonify({'message': 'Note created successfully', 'note_id': new_user_id})