from models.results import Result
from models.user_machine import UserMachine
from models.machines import Machine
from sqlalchemy import func

from models.users import User
from extensions import db
import datetime
class ResultRepository:
    
    @staticmethod
    def join_machine(machine_id, is_deleted,user_id):
        print("Joining machine repository method called")
        result = Result(machine_id=machine_id,created_date=datetime.datetime.now(),is_deleted=is_deleted  ,total_strips=0, faulty_strips=0, non_faulty_strips=0)
        db.session.add(result)
        db.session.commit()        
        query = (
        db.session.query(
            Result,
            User.id.label("user_id"),
            User.firstname.label("user_fname"),
            Machine.id.label("machine_id"),
            Machine.machine_code.label("machine_code")
            ).join(Machine, Machine.id == Result.machine_id)
            .join(UserMachine, UserMachine.machine_id == Machine.id)
            .join(User, User.id == UserMachine.user_id)
            .filter(Result.machine_id == machine_id)
            .filter(User.id == user_id)
            .filter(Machine.is_deleted == False)
            .filter(UserMachine.is_deleted == False)
            .order_by(Machine.created_date.desc())
        )        
        results = query.all()
        print("Result has been created and joined:", results)
        return results

    
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

        print(f"Here are all the machine_ids relation: {machine_ids}")
        print(f"All User-Machine Relations: {user_machines}")
        print(f"All Machines Assigned to User {user_id}: {machines}")
        
        return machine_ids
    
    @staticmethod
    def find_results_by_user_id(user_id):
        query = (
        db.session.query(
            Result,
            Machine,
            User
        )
        .join(Machine, Machine.id == Result.machine_id)
        .join(UserMachine, UserMachine.machine_id == Machine.id)
        .join(User, User.id == UserMachine.user_id)
        .filter(User.id == user_id)
        .filter(Machine.is_deleted == False)
        .filter(UserMachine.is_deleted == False)
        .order_by(Result.created_date.desc())
    )
    
        return query.all()

    
    @staticmethod
    def get_total_medicinal_strips(machine_ids):
        total = db.session.query(func.sum(Result.total_strips))\
            .filter(Result.machine_id.in_(machine_ids), Result.is_deleted == False)\
            .scalar() or 0
        return total

    
    @staticmethod
    def get_faulty_strips(machine_ids):
        total = db.session.query(func.sum(Result.faulty_strips))\
        .filter(Result.machine_id.in_(machine_ids), Result.is_deleted == False)\
        .scalar() or 0
        return total 

    @staticmethod
    def get_non_faulty_strips(machine_ids):
        total = db.session.query(func.sum(Result.non_faulty_strips))\
        .filter(Result.machine_id.in_(machine_ids), Result.is_deleted == False)\
        .scalar() or 0
        return total