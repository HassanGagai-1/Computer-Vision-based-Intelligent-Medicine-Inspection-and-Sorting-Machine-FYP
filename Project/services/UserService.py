from models.users import User
from dal.UserRepository import UserRepository
from argon2 import PasswordHasher
import logging
import resend
from flask import flash
import secrets
from itsdangerous import URLSafeTimedSerializer as Serializer
import datetime
import os
from extensions import mail
from flask_mail import Message
from flask import url_for
ph = PasswordHasher()
logger = logging.getLogger(__name__)
from argon2.exceptions import VerifyMismatchError
import sendgrid
from sendgrid.helpers.mail import (From, HtmlContent, Mail, PlainTextContent,
Subject, To)
class UserService:
    
    @staticmethod
    def register_user(firstname, lastname, email, password):
        if UserRepository.find_by_email(email):     
            raise ValueError("Email already exists")
        hashed_password = ph.hash(password)
        user = User(firstname, lastname, email, hashed_password)
        UserRepository.create_user(user)
        return user

    @staticmethod
    def login_user(email,password):
        logger.info(f"Attempting to find user with email: {email}")
        user = UserRepository.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        logger.info(f"User found via email: {user.firstname + ' ' + user.lastname}")
        
        logger.info(f"Attempting to verify password for {user.firstname + ' ' + user.lastname}")
        try:
            if ph.verify(user.password, password):
                return user
        except VerifyMismatchError:
            raise ValueError("Invalid email or password")
    
    @staticmethod
    def update_user(user_id, firstname, lastname, email):
        user = UserRepository.find_by_id(user_id)
        if user:
            UserRepository.update_user_detail(user, firstname, lastname, email)
        else:
            raise ValueError("User not found")
    
    @staticmethod
    def changepassword(user_mail, new_password):
        user = UserRepository.find_by_email(user_mail)
        if user:
            hashed_password = ph.hash(new_password)
            UserRepository.update_user(user.email,hashed_password)
        else:
            raise ValueError("User not found")
        
    @staticmethod
    def forget_password(email):
            user = UserRepository.find_by_email(email)
            if not user:
                flash('email has been sent, if the mail has not been received then invalid email', 'approved')
            
            if user:
                reset_token = secrets.token_urlsafe(32)
                reset_token_expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
                
                UserRepository.reset_token(user,reset_token, reset_token_expiry)
                reset_url = url_for('user.reset_password', token=reset_token, _external=True)
                msg = Message(
                    'Password Reset Request',
                    sender='bcsbs2112320@szabist.pk',
                    recipients=[user.email]
                )
                msg.body = f'Click the following link to reset your password: {reset_url}'
                mail.send(msg)
        
    @staticmethod
    def reset_password(user, password):
        if not user:
            raise ValueError("Invalid or expired token")
        hashed_password = ph.hash(password)
        user.password = hashed_password
        user.reset_token = None
        user.reset_token_expiry = None
        UserRepository.update_user(user)
        return user

    @staticmethod
    def get_user_profile(user_id):
        return UserRepository.find_by_id(user_id)
    
    @staticmethod
    def get_user_email_profile(email):
        return UserRepository.find_by_email(email)
    
    @staticmethod
    def get_secret_token(user_data_json):
        serial = Serializer(os.getenv('FLASK_SECRET_KEY', 'fallbacksecret'))
        # token = serial.dumps({'user_id': f'{user_id}'})
        token = serial.dumps(user_data_json)
        print('Token:', token)
        return token
    
    @staticmethod
    def send_email(useremail, html_subject ,html_content):
        FROM_EMAIL = 'hassangagai55@gmail.com'
        EMAIL_SUBJECT = html_subject
        HTML_CONTENT = html_content
        
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv('FLASK_SENDGRID_API_KEY'))
        message = Mail(
            from_email=From(FROM_EMAIL),
            to_emails=To(useremail),
            subject=Subject(EMAIL_SUBJECT),
            html_content=HtmlContent(HTML_CONTENT)
        )
        try:
            response = sg.send(message)
            print(response)
            return print({'message': 'Email sent successfully', 'response': response.status_code})
        except Exception as e:
            return print({'message': 'Failed to send email', 'error': str(e)})
        
    @staticmethod
    def delete_user(user):
        UserRepository.delete_user(user)