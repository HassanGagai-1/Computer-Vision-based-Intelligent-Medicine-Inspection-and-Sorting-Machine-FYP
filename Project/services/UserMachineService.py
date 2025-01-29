from dal.UserMachineRepository import UserMachineRepository
import logging
from models.user_machine import UserMachine
from flask import jsonify
logger = logging.getLogger(__name__)

class UserMachineService:
    @staticmethod
    def get_user_machines(current_user_id):
        return UserMachineRepository.find_user_machine(current_user_id)
    
    @staticmethod
    def delink_machine(machine_id,user_id):
        return UserMachineRepository.find_machine(machine_id,user_id)
        