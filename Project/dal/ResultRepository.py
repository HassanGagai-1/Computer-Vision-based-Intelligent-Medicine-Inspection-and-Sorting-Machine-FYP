from models.results import Result


class ResultRepository:
    @staticmethod
    def get_machine_info(machine_id):
        result = Result.query.filter_by(machine_id=machine_id).first()
        print(f"Query Result: {result}")
        return result
