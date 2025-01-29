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
    def find_machine_by_id(machine_id):
        machine = Machine.query.get(machine_id)
        if machine:
            machine.is_deleted = True
            db.session.commit(machine)
            db.session.commit()
            return machine
        else:
            return 404
        