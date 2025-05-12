from dal.ResultRepository import ResultRepository
from dal.UserMachineRepository import UserMachineRepository
class ResultService:
    @staticmethod
    def get_machine_info(machine_id):
        return ResultRepository.get_machine_info(machine_id)

    @staticmethod
    def get_total_medicinal_strips(user_ID):
        user_machineID = ResultRepository.get_all_user_machinesID(user_ID)
        if not user_machineID:
            return 0
        print("Here are userMachines ID" ,user_machineID)
        total = ResultRepository.get_total_medicinal_strips(user_machineID)

        print("Total Strips: ", total)
        return total
        
    @staticmethod
    def get_faulty_strips(user_id):
        user_machineID = ResultRepository.get_all_user_machinesID(user_id)
        if not user_machineID:
            return 0
        
        total = ResultRepository.get_faulty_strips(user_machineID)
        
        print("Total Faulty Strips: ", total)
        return total
    
    @staticmethod
    def get_non_faulty_strips(user_id):
        user_machineID = ResultRepository.get_all_user_machinesID(user_id)
        print("Getting USER MACHINES IDDSS",user_machineID)
        if not user_machineID:
            return 0
        total = ResultRepository.get_non_faulty_strips(user_machineID)
        
        print("Total non Faulty Strips: ", total)
        return total