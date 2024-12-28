from extensions import db

class Result(db.Model):
    __tablename__ = 'results'
    
    result_id = db.Column(db.Integer(), primary_key=True)
    machine_id = db.Column(db.Integer(), db.ForeignKey('machines.id'), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    is_deleted = db.Column(db.Boolean(), nullable=False)
    total_strips = db.Column(db.Integer(), nullable=False)
    fault_strips = db.Column(db.Integer(), nullable=False)
    non_faulty_strips = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return f'<Result {self.result_id} {self.machine_id}>'
    
    def __init__(self, machine_id, created_at, is_deleted, total_strips, fault_strips, Non_fault_strips):
        self.machine_id = machine_id
        self.created_at = created_at
        self.is_deleted = is_deleted
        self.total_strips = total_strips
        self.fault_strips = fault_strips
        self.Non_fault_strips = Non_fault_strips
    
    def to_dict(self):
        return {
            "result_id": self.result_id,
            "machine_id": self.machine_id,
            "created_at": self.created_at,
            "is_deleted": self.is_deleted,
            "total_strips": self.total_strips,
            "fault_strips": self.fault_strips,
            "Non_fault_strips": self.Non_fault_strips
        }