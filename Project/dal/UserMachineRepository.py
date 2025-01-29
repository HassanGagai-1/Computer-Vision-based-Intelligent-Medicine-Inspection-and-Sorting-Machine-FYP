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
        db.session.add(user_machine) 
        db.session.commit()
    
    @staticmethod
    def find_machine(machine_id,user_id):
        machine = UserMachine.query.filter_by(machine_id=machine_id, user_id=user_id).first()
        if not machine:
            return 404
        
        machine.is_deleted = True
        db.session.commit()
        return machine
        
    @staticmethod
    def delink_machine(machine_id,user_id):
        machine = (
            db.session.query(
                Machine.id,
                User.id
            )
            .join(User, User.id == Machine.created_by)
            .filter(UserMachine.machine_id == machine_id, UserMachine.user_id == user_id)
        )
        print("Delinking machine",machine)
        # query = query.filter(UserMachine.id == machine_id, User.id == user_id)
        if not machine:  # Handle if machine doesn't exist
            return 404
        machine.is_deleted = True
        db.session.commit()
        return machine
        