from models.users import User
from dal.UserRepository import UserRepository
from argon2 import PasswordHasher
import logging
ph = PasswordHasher()
logger = logging.getLogger(__name__)

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
        if ph.verify(user.password, password):
            return user
        return ValueError("Invalid email or password")