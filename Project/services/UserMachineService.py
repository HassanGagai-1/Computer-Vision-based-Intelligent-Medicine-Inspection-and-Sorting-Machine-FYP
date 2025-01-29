from dal.UserMachineRepository import UserMachineRepository
import logging
from models.user_machine import UserMachine

logger = logging.getLogger(__name__)

class UserMachineService:
    @staticmethod
    def get_user_machines(current_user_id):
        return UserMachineRepository.find_user_machine(current_user_id)
    
    @staticmethod
    def find_machine_delink(machine_id):
        machine = UserMachineRepository.find_machine_by_id(machine_id)
        if machine == 404:
            return jsonify({"error": "Machine not found"}), 404
        else:
            return jsonify({"success": "Machine found"}), 200
        
        