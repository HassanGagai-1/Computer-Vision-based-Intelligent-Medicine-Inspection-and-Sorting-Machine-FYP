from models.machines import Machine
from dal.MachineRepository import MachineRepository
from dal.UserMachineRepository import UserMachineRepository
from dal.UserRepository import UserRepository
import logging
from extensions import db
from flask import jsonify

from models.user_machine import UserMachine
logger = logging.getLogger(__name__)

class MachineService:
    @staticmethod
    def register_machine(current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img):
        created_by = UserRepository.find_user_name_by_id(current_user_id)
        print("User Created by", created_by)
        machine = Machine(machine_name,machine_password,machine_code, created_by, machine_description, machine_profile_img)
        MachineRepository.create_machine(machine)
        
        # user_machine = UserMachine(user_id=current_user_id, machine_id = machine.id)
        # MachineRepository.create_user_machine(user_machine)
        
        return machine
    
    @staticmethod
    def find_machine_and_link(machine_code, machine_password, current_user_id):
        machine = MachineRepository.find_by_machine_code(machine_code)
        if not machine:
            return 404
        elif machine.machine_password != machine_password:
            return 403
        else:
            user_machine = UserMachine(user_id=current_user_id, machine_id = machine.id, is_deleted = False)
            UserMachineRepository.create_user_machine(user_machine)
            return machine.to_dict()

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