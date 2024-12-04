from models.users import User
from dal.UserRepository import UserRepository
from argon2 import PasswordHasher


ph = PasswordHasher()

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
        user = UserRepository.find_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")
        print(f"User found: {user}")
        
        if ph.verify(user.password, password):
            return user
        else:
            raise ValueError("Invalid email or password")

