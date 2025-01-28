from models.machines import Machine
from dal.MachineRepository import MachineRepository
import logging
from extensions import db
from flask import jsonify

from models.user_machine import UserMachine
logger = logging.getLogger(__name__)

class MachineService:
    @staticmethod
    def register_machine(machine_code, created_by, current_user_id):
        machine = Machine(machine_code, created_by)
        MachineRepository.create_machine(machine)
        
        user_machine = UserMachine(user_id=current_user_id, machine_id = machine.id)
        MachineRepository.create_user_machine(user_machine)
        
        return machine
    
    @staticmethod
    def find_machine(machine_code, machine_password):
        machine = MachineRepository.find_by_machine_code(machine_code)
        if not machine:
            return 404
        elif machine.machine_password != machine_password:
            return 403
        else:
            return machine
    
    @staticmethod
    def get_machine_info(machine_code):
        return MachineRepository.find_by_machine_code(machine_code)
    
    @staticmethod
    def get_machine_info_by_id(machine_id):
        return MachineRepository.find_by_id(machine_id)
        
    @staticmethod
    def machine_verification(machine_id):
        Machine = MachineRepository.find_by_id(machine_id)
        if not Machine:
            return ValueError("Machine not found")
        else:
            return Machine

    @staticmethod
    def update_machine(machine_code, updated_by, machine_id):
        machine = MachineRepository.find_by_id(machine_id)
        if not machine:
            raise ValueError('Machine not found')
        else:
            MachineRepository.update_machine(machine, machine_code, updated_by)

    @staticmethod
    def delete_machine(machine):
        deleted = MachineRepository.delete_machine(machine)
        if deleted:
            return True
        else:
            db.session.rollback()
            return False