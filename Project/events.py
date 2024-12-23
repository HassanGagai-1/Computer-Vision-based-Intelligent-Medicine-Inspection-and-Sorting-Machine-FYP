from sqlalchemy import event
from sqlalchemy.orm import Session
from models import users

@event.listens_for(Session, "before_flush")
def validate_user_data(session):
    for obj in session.new:
        if isinstance(obj, users):
            if '@' not in obj.email:
                raise ValueError("Invalid email format")
            if len(obj.password) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if obj.firstname == obj.lastname:
                raise ValueError("First name and last name must be different")
            
