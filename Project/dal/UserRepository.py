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
        user =  User.query.get(user_id)
        if user:
            print(f"User found for id {user_id}: {user.email}")
            return user
        else:
            print(f"No user found for id {user_id}")
            
    @staticmethod
    def find_user_name_by_id(user_id):
        user = db.session.query(User.firstname, User.lastname).filter(User.id == user_id).first()
        
        if user:
            print(f"User found for id {user_id}: {user.firstname} {user.lastname}")
            return user.firstname + " " + user.lastname
        else:
            print(f"No user found for id {user_id}")
            return None

    
    @staticmethod
    def update_user_detail(user, firstname, lastname, email):
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        db.session.commit()
    
    @staticmethod
    def update_user(user_mail, hashed_password ):
        db.session.query(User).filter_by(email=user_mail).update({'password': hashed_password})
        db.session.commit()
        
    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()

