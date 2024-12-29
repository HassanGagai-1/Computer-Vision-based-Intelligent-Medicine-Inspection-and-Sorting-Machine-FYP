from models.machines import Machine
from extensions import db

class MachineRepository:
    @staticmethod
    def find_by_machine_code(machine_code):
        machine = Machine.query.filter_by(machine_code=machine_code).first()
        return machine

    @staticmethod
    def find_machine_password(machine_password):
        machine = Machine.query.filter_by(machine_password=machine_password).first()
        return machine
    
    @staticmethod
    def create_machine(machine):
        db.session.add(machine)
        db.session.commit()

    @staticmethod
    def find_all():
        return Machine.query.all()
    
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