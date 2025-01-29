from models.machines import Machine
from dal.MachineRepository import MachineRepository
from dal.UserMachineRepository import UserMachineRepository
from dal.UserRepository import UserRepository
import logging
from extensions import db
from flask import jsonify
import datetime
from models.user_machine import UserMachine
logger = logging.getLogger(__name__)

class MachineService:
    
    @staticmethod
    def register_machine(current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img):
        print("User Created by", current_user_id)
        if not machine_code:
            raise ValueError("Machine code cannot be empty")
        machine = Machine(
                machine_name=machine_name,
                machine_code=machine_code,
                created_by=current_user_id,
                updated_by=current_user_id,
                machine_password=machine_password,
                machine_description=machine_description,
                machine_profile_img=machine_profile_img
            )
        MachineRepository.create_machine(machine)
        
        # user_machine = UserMachine(user_id=current_user_id, machine_id = machine.id)
        # MachineRepository.create_user_machine(user_machine)
        
        return machine
    
    @staticmethod
    def update_admin_machine(machine_id,current_user_id,machine_name,machine_password,machine_code,machine_description,machine_profile_img):
        machine = MachineRepository.find_by_machine_id(machine_id)
        if not machine:
            raise ValueError('Machine not found')
        
        print("MACHINE HAS BEEN FOUND", machine)
        machine.machine_name = machine_name
        machine.machine_password = machine_password
        machine.machine_description = machine_description
        machine.machine_profile_img = machine_profile_img
        machine.updated_by = current_user_id
        machine.updated_date = datetime.datetime.now()
        MachineRepository.update_machine(machine)
    
    @staticmethod
    def find_machine_and_link(machine_code, machine_password, current_user_id):
        machine = MachineRepository.find_by_machine_code(machine_code)
        if not machine:
            return 404
        elif machine.machine_password != machine_password:
            return 403
        elif machine.is_deleted == True:
            return 401
        else:
            user_machine = UserMachine(user_id=current_user_id, machine_id = machine.id, is_deleted = False)
            UserMachineRepository.create_user_machine(user_machine)
            return machine.to_dict()

    @staticmethod
    def get_all_machines():
        
        return MachineRepository.get_all_machines()
    
    def get_by_ID(machine_id,user_id):
        return MachineRepository.find_by_id(machine_id,user_id)
        
    
    @staticmethod
    def get_machine_info(machine_code):
        return MachineRepository.find_by_machine_code(machine_code)
    
    @staticmethod
    def get_machine_info_by_id(machine_id):
        return MachineRepository.find_by_id(machine_id)
        
    @staticmethod
    def machine_verification(machine_id,user_id):
        Machine = MachineRepository.find_by_id(machine_id,user_id)
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