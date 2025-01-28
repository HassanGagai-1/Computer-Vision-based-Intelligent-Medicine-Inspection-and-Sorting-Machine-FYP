from extensions import db

class Result(db.Model):
    __tablename__ = 'result'
    
    result_id = db.Column(db.Integer(), primary_key=True)
    machine_id = db.Column(db.Integer(), nullable=False)
    created_date = db.Column(db.DateTime(), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=True)
    total_strips = db.Column(db.Integer(), nullable=True)
    faulty_strips = db.Column(db.Integer(), nullable=True)
    non_faulty_strips = db.Column(db.Integer(), nullable=True)
    
    def __repr__(self):
        return f'<Result {self.result_id} {self.machine_id}>'
    
    def __init__(self, machine_id, created_date, is_deleted, total_strips, faulty_strips, non_faulty_strips):
        self.machine_id = machine_id
        self.created_date = created_date
        self.is_deleted = is_deleted
        self.total_strips = total_strips
        self.faulty_strips = faulty_strips
        self.non_faulty_strips = non_faulty_strips
    
    def to_dict(self):
        return {
            "result_id": self.result_id,
            "machine_id": self.machine_id,
            "created_date": self.created_date,
            "is_deleted": self.is_deleted,
            "total_strips": self.total_strips,
            "faulty_strips": self.faulty_strips,
            "non_faulty_strips": self.non_faulty_strips
        }