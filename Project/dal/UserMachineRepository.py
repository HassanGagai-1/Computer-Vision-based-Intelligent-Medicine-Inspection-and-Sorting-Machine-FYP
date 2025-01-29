from extensions import db
from models.user_machine import UserMachine
from models.users import User
from models.machines import Machine

class UserMachineRepository:
    
    @staticmethod
    def find_user_machine(current_user_id):
        return User.query.get(current_user_id)
    
    @staticmethod
    def create_user_machine(user_machine):
        # Check if the user and machine can be linked by performing a JOIN query
        user_alias = aliased(User)  # Alias for user table

        # Perform the SQL equivalent join check
        result = db.session.query(User, UserMachine, Machine).\
            join(UserMachine, and_(
                User.id == UserMachine.user_id,
                UserMachine.is_deleted == False,
                UserMachine.machine_id == user_machine.machine_id
            )).\
            join(Machine, and_(
                Machine.id == user_machine.machine_id,
                Machine.is_deleted == False
            )).\
            filter(User.id == user_machine.user_id).\
            first()  # Only want to check if a match exists

        # If the result exists, it means the user can be linked to the machine
        if result:
            db.session.add(user_machine)  # Add the new user-machine link
            db.session.commit()
            return user_machine
        else:
            # If no match, return an error or some other behavior (like raising an exception)
            raise ValueError("Cannot link this user to the machine. Invalid user or machine.")
