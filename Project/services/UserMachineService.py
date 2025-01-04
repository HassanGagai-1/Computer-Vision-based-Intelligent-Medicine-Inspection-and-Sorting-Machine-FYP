from dal.UserMachineRepository import UserMachineRepository
import logging


logger = logging.getLogger(__name__)

class UserMachineService:
    @staticmethod
    def get_user_machines(current_user_id):
        return UserMachineRepository.find_user_machine(current_user_id)
    