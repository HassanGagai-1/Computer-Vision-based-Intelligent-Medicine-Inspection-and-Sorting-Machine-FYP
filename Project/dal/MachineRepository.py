from models.machines import Machine
from extensions import db
from models.results import Result
import logging
from models.users import User  
logger = logging.getLogger(__name__)

class MachineRepository:
    
    
    @staticmethod
    def get_all_machines(created_by):
        query = (
            db.session.query(
                Machine.id, 
                Machine.machine_name, 
                Machine.machine_code, 
                Machine.machine_password, 
                User.firstname
            )
            .join(User, User.id == Machine.created_by)
            .filter(Machine.is_deleted == False)
            .filter(Machine.created_by == created_by)
            .order_by(Machine.created_date.desc())
        )

        if created_by:
            query = query.filter(Machine.created_by == created_by)

        return query.all()
    
    @staticmethod
    def find_by_machine_id(id):
        return Machine.query.filter_by(id=id).first()

    @staticmethod
    def find_by_machine_code(machine_code):
        return Machine.query.filter_by(machine_code=machine_code).first()
    
    @staticmethod
    def find_machine_password(machine_password):
        return Machine.query.filter_by(machine_password=machine_password).first()

    @staticmethod
    def create_machine(machine):
        db.session.add(machine)
        db.session.commit()

    @staticmethod
    def create_user_machine(user_machine):
        db.session.add(user_machine)
        db.session.commit()

    @staticmethod
    def find_by_id(machine_id,user_id):
        return Machine.query.filter_by(id=machine_id, created_by = user_id, is_deleted=False).first()
    
    @staticmethod
    def update_machine(machine):
        # machine.machine_code = machine_code
        # machine.updated_by = updated_by
        db.session.commit()
    
    @staticmethod
    def delete_machine(machine):
        machine.is_deleted = True
        # db.session.update(machine)
        db.session.commit()
        return machine.is_deleted