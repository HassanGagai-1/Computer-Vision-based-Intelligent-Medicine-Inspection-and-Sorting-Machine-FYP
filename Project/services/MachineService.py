from models.machines import Machine
from dal.MachineRepository import MachineRepository
import logging
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
    def get_machine_info(machine_code):
        return MachineRepository.find_by_machine_code(machine_code)