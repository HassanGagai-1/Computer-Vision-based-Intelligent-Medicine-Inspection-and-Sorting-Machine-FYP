from dal.ResultRepository import ResultRepository
from dal.UserMachineRepository import UserMachineRepository
class ResultService:
    @staticmethod
    def get_machine_info(machine_id):
        return ResultRepository.get_machine_info(machine_id)

    @staticmethod
    def get_total_medicinal_strips(user_ID):
        total_strips = 0
        user_machineID = ResultRepository.get_all_user_machinesID(user_ID)
        
        for um in user_machineID:
            print("Here are userMachines ID" ,um)
            strips = ResultRepository.get_total_medicinal_strips(um)
            if strips is None:
                print(f"No strips found for machine {um}")
                continue
            total_strips += strips       

        print("Total Strips: ", total_strips)
        return total_strips
        
    @staticmethod
    def get_faulty_strips(user_id):
        total_faulty_strips = 0
        user_machineID = ResultRepository.get_all_user_machinesID(user_id)
        
        for um in user_machineID:
            faulty_strips = ResultRepository.get_faulty_strips(um)
            if faulty_strips is None:
                print(f"No strips found for machine {um}")
                continue
            total_faulty_strips += faulty_strips
        
        print("Total Faulty Strips: ", total_faulty_strips)
        return total_faulty_strips
    
    @staticmethod
    def get_non_faulty_strips(user_id):
        total_non_faulty_strips = 0
        user_machineID = ResultRepository.get_all_user_machinesID(user_id)
        
        for um in user_machineID:
            non_faulty_strips = ResultRepository.get_non_faulty_strips(um)
            if non_faulty_strips is None:
                print(f"No strips found for machine {um}")
                continue
            total_non_faulty_strips += non_faulty_strips
        
        print("Total non Faulty Strips: ", total_non_faulty_strips)
        return total_non_faulty_strips