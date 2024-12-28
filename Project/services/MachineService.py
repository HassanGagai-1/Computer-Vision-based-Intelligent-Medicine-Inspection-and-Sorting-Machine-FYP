from models.machines import Machine
from dal.MachineRepository import MachineRepository
from argon2 import PasswordHasher
import logging
ph = PasswordHasher()
logger = logging.getLogger(__name__)

class MachineService:
    
    @staticmethod
    def add_machine(machine_code, machine_name):
        if MachineRepository.find_by_machine_code(machine_code):
            raise ValueError("Machine already exists")
        machine = Machine(machine_code, machine_name)
        MachineRepository.create_machine(machine)
        return machine
        
    @staticmethod
    def get_machines():
        machine = MachineRepository.find_all()
        if not machine:
            raise ValueError("Machine not found")
        return machine
    
    
    @staticmethod
    def register_machine(machine_code, machine_password, created_by):
        if MachineRepository.find_by_machine_code(machine_code):
            raise ValueError("Machine already exists")
        hashed_password = ph.hash(machine_password)
        machine = Machine(machine_code, hashed_password, created_by)
        MachineRepository.create_machine(machine)
        return machine

    @staticmethod
    def login_machine(machine_code,machine_password):
        logger.info(f"Attempting to find machine with machine_code: {machine_code}")
        machine = MachineRepository.find_by_machine_code(machine_code)
        if not machine:
            raise ValueError("Invalid machine_code or machine_password")
        logger.info(f"Machine found via machine_code: {machine.machine_code}")
        
        logger.info(f"Attempting to verify password for {machine.machine_code}")
        if ph.verify(machine.machine_password, machine_password):
            return machine
        return ValueError("Invalid machine_code or machine_password")