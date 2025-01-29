from models.machines import Machine
from extensions import db
from models.results import Result
import logging
from models.users import User  
logger = logging.getLogger(__name__)

class MachineRepository:
    @staticmethod
    def get_all_machines(created_by=None):
        query = db.session.query(
            Machine.id,
            Machine.machine_name,
            Machine.machine_code,
            Machine.machine_description,
            Machine.created_date,
            Machine.updated_date,
            Machine.is_deleted,
            User.id.label("created_by"),  # ✅ Fetch user ID
            User.firstname,  # ✅ Fetch user first name
            User.lastname   # ✅ Fetch user last name
        ).join(User, User.id == Machine.created_by) \
         .filter(Machine.is_deleted == False) \
         .order_by(Machine.created_date.desc())

        # ✅ Filter only if created_by is provided
        if created_by:
            query = query.filter(Machine.created_by == created_by)

        return query.all()

    
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
    def find_by_id(machine_id):
        return Machine.query.get(machine_id)
    
    @staticmethod
    def update_machine(machine, machine_code, updated_by):
        machine.machine_code = machine_code
        machine.updated_by = updated_by
        db.session.update(machine)
        db.session.commit()
    
    @staticmethod
    def delete_machine(machine):
        machine.is_deleted = True
        db.session.update(machine)
        db.session.commit()
        return machine.is_deleted