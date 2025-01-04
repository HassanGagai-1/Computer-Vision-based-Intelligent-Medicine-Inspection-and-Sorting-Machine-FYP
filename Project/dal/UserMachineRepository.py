from extensions import db
from models.user_machine import UserMachine
from models.users import User
from models.machines import Machine

class UserMachineRepository:
    
    @staticmethod
    def find_user_machine(current_user_id):
        return User.query.get(current_user_id)
    