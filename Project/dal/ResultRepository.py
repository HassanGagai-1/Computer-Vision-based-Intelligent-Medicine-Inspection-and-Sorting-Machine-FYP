from models.results import Result
from models.user_machine import UserMachine
from models.machines import Machine
class ResultRepository:
    @staticmethod
    def get_machine_info(machine_id):
        result = Result.query.filter_by(machine_id=machine_id).first()
        print(f"Query Result: {result}")
        return result

    @staticmethod
    def get_all_user_machinesID(user_id):
        user_machines  = UserMachine.query.filter_by(user_id=user_id).all()
        machine_ids = [um.machine_id for um in user_machines]
        machines = Machine.query.filter(Machine.id.in_(machine_ids)).all()

        print(f"All User-Machine Relations: {user_machines}")
        print(f"All Machines Assigned to User {user_id}: {machines}")
        
        return machine_ids
    
    @staticmethod
    def get_total_medicinal_strips(user_machineID):
        result = Result.query.filter_by(machine_id=user_machineID).first()
        medicinal_strips = result.total_strips
        print("Here are medicinal Strips: ", medicinal_strips)
        return medicinal_strips
    
    @staticmethod
    def get_faulty_strips(user_machineID):
        result = Result.query.filter_by(machine_id=user_machineID).first()
        faulty_strips = result.faulty_strips
        print("Here are faulty Strips: ", faulty_strips)
        return faulty_strips

    @staticmethod
    def get_non_faulty_strips(user_machineID):
        result = Result.query.filter_by(machine_id=user_machineID).first()
        non_faulty_strips = result.non_faulty_strips
        print("Here are non-faulty Strips: ", non_faulty_strips)
        return non_faulty_strips