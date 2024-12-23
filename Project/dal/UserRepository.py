from models.users import User
from extensions import db

class UserRepository:
    @staticmethod
    def find_by_email(email):
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found for email {email}: {user.firstname}")
        else:
            print(f"No user found for email {email}")
        return user

    @staticmethod
    def create_user(user):
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def update_user(user):
        db.session.update(user)
        db.session.commit()
    
    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

