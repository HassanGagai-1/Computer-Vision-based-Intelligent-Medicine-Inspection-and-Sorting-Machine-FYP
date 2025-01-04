from dal.ResultRepository import ResultRepository

class ResultService:
    @staticmethod
    def get_machine_info(machine_id):
        return ResultRepository.get_machine_info(machine_id)
