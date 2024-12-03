from models.users import User
from extensions import db

class UserRepository:
    @staticmethod
    def find_by_email(email):
        user = User.query.filter_by(email=email).first()
        print(f"User found for email {email}: {user}")
        return user

    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)