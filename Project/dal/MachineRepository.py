from models.machines import Machine
from extensions import db

class MachineRepository:
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
    def update_machine(machine):
        db.session.update(machine)
        db.session.commit()
    
    @staticmethod
    def delete_machine(machine):
        db.session.delete(machine)
        db.session.commit()