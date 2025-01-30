from extensions import db
from models.user_machine import UserMachine
from models.users import User
from models.machines import Machine

class UserMachineRepository:
    
    @staticmethod
    def get_user_machines(current_user_id):
        user_machines = (
        db.session.query(UserMachine.machine_id)
        .filter(UserMachine.user_id == current_user_id, UserMachine.is_deleted == False)
        .all()
        )

        # Extract machine IDs
        machine_ids = [um.machine_id for um in user_machines]
        
        if not machine_ids:
            return []  # No machines found

        # Fetch machine details from Machine table
        machines = (
            db.session.query(Machine)
            .filter(Machine.id.in_(machine_ids), Machine.is_deleted == False)
            .all()
        )

        return [
            {
                "id": machine.id,
                "machine_code": machine.machine_code,
                "machine_name": machine.machine_name,
                "created_by": machine.created_by,
                "created_date": machine.created_date,
                "updated_date": machine.updated_date,
                "updated_by": machine.updated_by,
                "machine_description": machine.machine_description,
                "machine_profile_img": machine.machine_profile_img
            }
            for machine in machines
        ]


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
        